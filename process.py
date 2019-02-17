from pydub import AudioSegment


sound1 = AudioSegment.from_file("./src/datas/train/test3.wav", format="wav")
# add 6 db
louder = sound1 + 15

file_handle = louder.export("./src/datas/train/test3-more.wav", format="wav")
