
import numpy as np
import random
from pydub import AudioSegment
from pydub.utils import mediainfo

def load_file(path):
    sound = AudioSegment.from_file(path)
    print(path)
    print(mediainfo(path))
    return sound


def fill_to_1sec(wav):
    #fill to 1 second
    L = 1000 #16000  # 1 sec
    sample_rate = 16000
    
    if len(wav) > L:
        i = np.random.randint(0, len(wav) - L)
        wav = wav[i:(i+L)]
    elif len(wav) < L:
        rem_len = L - len(wav)
        wav = AudioSegment.silent(rem_len,frame_rate=sample_rate) + wav
        
    return wav    


def speed_change(sound, speed=1.0):
	# Manually override the frame_rate. This tells the computer how many
	# samples to play per second
	sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
		"frame_rate": int(sound.frame_rate * speed)
	})


	# slow_sound = speed_change(sound, 0.75)
	# fast_sound = speed_change(sound, 2.0)

	# convert the sound with altered frame rate to a standard frame rate
	# so that regular playback programs will work right. They often only
	# know how to play audio at standard frame rate (like 44.1k)
	return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def augment_wav(wav,pval=0.5):
    sample_rate = 16000
    L = 1000 #16000  # 1 sec
    
#     adjust speed, with 50% chance
    wav = speed_change(wav,1.+ random.choice([.1,-0.1,0])) #random.uniform(-1, 1)*0.05) if np.random.random() < pval else wav
    
    
    #adjust volume
#     db_adjustment = random.uniform(-1, 1)*10
    wav = wav + random.choice([-10,-5,0,5,10]) #randodb_adjustment if np.random.random() < pval else wav
     
        
    #fill to 1 second
    wav = fill_to_1sec(wav)        
        
    #shift the audio by 10 ms
    shift_length = 100
    if np.random.random() < 0.5: #shift to left
        wav = wav[:L-shift_length]+ AudioSegment.silent(shift_length,frame_rate=sample_rate)
    else: #shift to right
        wav = AudioSegment.silent(shift_length,frame_rate=sample_rate) + wav[shift_length:]
        
        
        
    #blend original file with background noise     
#     if np.random.random() < pval:
    noise = random.choice(load_file("datas/train/bg1.wav"))
    db_delta = (wav.dBFS - noise.dBFS) -10.

    if db_delta< 0: #reduce intensity of loud background; if it's too silent, leave it be
        noise = noise  + db_delta
    wav = wav.overlay(noise)
 
    return wav