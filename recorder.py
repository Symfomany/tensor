# -*- coding: utf-8 -*-
'''recorder.py
Provides WAV recording functionality via two approaches:
Blocking mode (record for a set duration):
>>> rec = Recorder(channels=2)
>>> with rec.open('blocking.wav', 'wb') as recfile:
...     recfile.record(duration=5.0)
Non-blocking mode (start and stop recording):
>>> rec = Recorder(channels=2)
>>> with rec.open('nonblocking.wav', 'wb') as recfile2:
...     recfile2.start_recording()
...     time.sleep(5.0)
...     recfile2.stop_recording()
'''
import pyaudio
import wave
import struct
import math
from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 16000  
INPUT_BLOCK_TIME = 0.075
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
INITIAL_TAP_THRESHOLD = 0.010
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME # if we get this many quiet blocks in a row, decrease the threshold
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME # if the noise was longer than this many blocks, it's not a 'tap'


class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=16000, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        print("Go Record in Streaming...")
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)

        ###
        # Init quiet and noisy
        ###

        tap_threshold = INITIAL_TAP_THRESHOLD                  #]
        noisycount = MAX_TAP_BLOCKS+1                          #|---- Variables for noise detector...
        quietcount = 0                                         #|
        errorcount = 0   

        for _ in range(int(self.rate / self.frames_per_buffer * duration)): # time to record
            audio = self._stream.read(self.frames_per_buffer)
            amplitude = self.get_rms(audio) # Root mean Square va permettre de calculer l'amplitude d'un son en streaming
            print("Amplitude RMS (x100) ... ", amplitude * 1000)

            if amplitude* 1000 > 10: 
                print("C'est trop fort !")
                
            if amplitude > tap_threshold: # if its to loud... bruyant
                quietcount = 0
                noisycount += 1
                if noisycount > OVERSENSITIVE:
                    tap_threshold *= 1.1 # turn down the sensitivity

            else: # if its to quiet...
                if 1 <= noisycount <= MAX_TAP_BLOCKS:
                    print("** Son**")
                noisycount = 0
                quietcount += 1
                if quietcount > UNDERSENSITIVE:
                    tap_threshold *= 0.9 # turn up the sensitivity
            self.wavefile.writeframes(audio) # write iun real time
        return None

        
    def get_rms(self,block):

        # RMS amplitude is defined as the square root of the 
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into 
        # a string of 16-bit samples...

        # we will get one short out for each 
        # two chars in the string.
        count = len(block)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, block )

        ## Unpack from the buffer buffer (presumably packed by pack(format, ...)) according to the format string format. The result is a tuple even if it contains exactly one item. The buffer’s size in bytes must match the size required by the format, as reflected by calcsize().

        # iterate over the block.
        sum_squares = 0.0
        for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
            n = sample * (1.0/32768.0)
            sum_squares += n*n

        return math.sqrt( sum_squares / count )


    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        print("End Record in Streaming !")
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()
        sound1 = AudioSegment.from_file(self.fname, format="wav")
        # add 6 db
        louder = sound1 + 15
    
        start_trim = self.detect_leading_silence(louder)
        end_trim = self.detect_leading_silence(louder.reverse())
        duration = len(louder)    
        trimmed_sound = louder[start_trim:duration-end_trim]
        print(louder)
        print(trimmed_sound)
        trimmed_sound.export(self.fname, format="wav")
        print('Close file trimmed and exported with += 15dB')

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

    def detect_leading_silence(self,sound, silence_threshold=-55.0, chunk_size=10):
        '''
        sound is a pydub.AudioSegment
        silence_threshold in dB
        chunk_size in ms
        iterate over chunks until you find the first one with sound
        '''
        trim_ms = 0 # ms

        assert chunk_size > 0 # to avoid infinite loop
        while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
            trim_ms += chunk_size

        return trim_ms

    def draw(self):
        # Wave Plot
        filename = librosa.util.example_audio_file()
        y, sr = librosa.load(self.fname)
        plt.figure()
        plt.subplot(3, 1, 1)
        librosa.display.waveplot(y, sr=sr)
        plt.title('Monophonic')
        plt.show()

        # MFCC
        
        D = np.abs(librosa.stft(y))**2
        S = librosa.feature.melspectrogram(S=D)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S,ref=np.max), y_axis='mel', fmax=8000,x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        plt.show()


