#!/usr/bin/python

import argparse, sys, os

import tensorflow as tf
from keras import backend as K

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import (
    tag_constants,
    signature_constants,
    signature_def_utils_impl,
)

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np
import pandas as pd


from python_speech_features import mfcc
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from matplotlib import cm

from utils import augment_wav, load_file


def main(_):
    (rate, sig) = wav.read("./datas/train/Enregistrement (12).wav")
    # chunk_id = wav.read("./datas/train/Enregistrement (12).wav")  # See the WAVE file format docs
    mfcc_feat = mfcc(sig, rate)  # mfcc wave

    ig, ax = plt.subplots()
    mfcc_data = np.swapaxes(mfcc_feat, 0, 1)
        # Parse experiment settings
    settings = pd.read_csv(FLAGS.settings)
    # print(settings.steps[1])
    cax = ax.imshow(
        mfcc_data,
        interpolation="nearest",
        cmap=cm.coolwarm,
        origin="lower",
        aspect="auto",
    )
    ax.set_title("MFCC")
    # Showing mfcc_data
    plt.show()

    # Showing mfcc_feat
    # plt.plot(mfcc_feat)
    # plt.show()


def info():
    (rate, sig) = wav.read("./datas/train/Enregistrement (29).wav")
    print(rate)        

def train():
    # Creates a learn session
    sess = tf.Session()
    K.set_session(sess)
    K.set_learning_phase(0)

    # Set Variables
    model_version = "3"
    epoch = 100

    # Load up data
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = np.array([[0], [1], [1], [0]])
    print(X, Y)

    # Build the Model
    model = Sequential()
    model.add(Dense(8, input_dim=2))
    model.add(Activation("tanh"))
    model.add(Dense(1))
    model.add(Activation("sigmoid"))
    sgd = SGD(lr=0.1)

    # Compile and fit the model
    model.compile(loss="binary_crossentropy", optimizer=sgd)
    model.fit(X, Y, batch_size=1, nb_epoch=epoch)

    # Get Tensorflow Serving Input and Output variables
    x = model.input
    y = model.output
    prediction_signature = tf.saved_model.signature_def_utils.predict_signature_def(
        {"inputs": x}, {"prediction": y}
    )
    print("prediction : ", prediction_signature)

    # Test if the prediction signature for tf serving is valid
    valid_prediction_signature = tf.saved_model.signature_def_utils.is_valid_signature(
        prediction_signature
    )
    if valid_prediction_signature == False:
        raise ValueError("Error: Prediction signature not valid!")
    print("Validation : ", valid_prediction_signature)

    # Build and confiugure model
    builder = saved_model_builder.SavedModelBuilder("./" + model_version)
    legacy_init_op = tf.group(tf.tables_initializer(), name="legacy_init_op")
    builder.add_meta_graph_and_variables(
        sess,
        [tag_constants.SERVING],
        signature_def_map={
            signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature
        },
        legacy_init_op=legacy_init_op,
    )

    builder.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/datas/train/',
      help="""\
      Directory of files used for training.
      """)
    parser.add_argument('--architecture', type=str, default='vgg',
      help="""\
      Model architecture to use.
      """)
    parser.add_argument('--optimizer', type=str, default='gd',
      help="""\
      Optimizer to use.
      """)
    parser.add_argument('--summaries_dir', type=str, default='train_logs',
      help="""\
      Optimizer to use.
      """)
    parser.add_argument('--train_dir', type=str, default='/tmp/isaac',
      help="""\
      Directory to write checkpoints to.
      """)
    parser.add_argument('--log_alias', type=str, default='isaac',
      help="""\
      Optimizer to use.
      """)
    parser.add_argument('--start_checkpoint', type=str, default='',
      help="""\
      Optimizer to use.
      """)
    parser.add_argument('--settings', type=str, default='./settings.csv',
       help="""\
       How many training steps.
       """)
    parser.add_argument('--batch_size', type=int, default=128,
       help="""\
       Batch size.
       """)
    parser.add_argument('--evaluation_step', type=int, default=400,
       help="""\
       How frequently we need to check the validation score.
       """)
    parser.add_argument('--save_step_interval', type=int, default=400,
       help="""\
       How frequently we need to save the checkpoint.
       """)
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)


