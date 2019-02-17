import recorder as rec
import time
import argparse, sys, os
import tensorflow as tf

print("Enregistrement de samples 16000Hz (sr) 1024bits(bd) WAV ")

print("Commencement dans 1 sec... Prêt ?")
time.sleep(1)


def main(_):
    for i in range(0,FLAGS.nb_samples):
        print("Enregistrement numéro {nb}".format(nb=i))
        file = "{dir}test{nb}.wav".format(nb=i, dir=FLAGS.data_dir)
        file = rec.Recorder().open(fname=file)
        file.record(FLAGS.duration)
        file.draw()
        file.close()
        print("Pause 1 sec...")
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nb_samples', type=int, default=5,
      help="""\
        Nb of samples for training.
      """)
    parser.add_argument('--duration', type=float, default=2.2,
      help="""\
        Duration of samples
      """)
    parser.add_argument('--data_dir', type=str, default='./src/datas/train/',
      help="""\
        Directory of files used for training.
      """)
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

