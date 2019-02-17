import tensorflow as tf
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio

filename = "./datas/train/Enregistrement (12).wav"
audio_binary = tf.read_file(filename)
desired_channels = 1
wav_decoder = contrib_audio.decode_wav(
    audio_binary,
    desired_channels=desired_channels)