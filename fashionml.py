import tensorflow as tf
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist
import keras
import os
import imageio
import struct
import gzip

print(tf.__version__)

(train_images, train_labels), (test_images,
                               test_labels) = tf.keras.datasets.fashion_mnist.load_data()


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# class_names = ['chien' 'chat']

# Checkpoint Path
checkpoint_path = "./checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

print(train_images.shape)  # (60000, 28, 28) -> 70000 mais test 10000

# print(train_labels)

# arr = imageio.imread("./trained/train/ankle_boot.jpg")


def read_idx(filename):
    with gzip.open(filename) as f:
        zero, data_type, dims = struct.unpack('>HBB', f.read(4))
        shape = tuple(struct.unpack('>I', f.read(4))[0] for d in range(dims))
        return np.fromstring(f.read(), dtype=np.uint8).reshape(shape)


img_test = read_idx("./trained/train/ankle_boot.jpg.gz")
# print(img_test)
test_images.append(img_test)

print(test_images.shape)  # (60000, 28, 28) -> 70000 mais test 10000

exit()

# Display first image
# that the pixel values fall in the range of 0 to 255:
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
# plt.show()

# We scale these values to a range of 0 to 1 before feeding to the neural network model.
# For this, we divide the values by 255. The red, green and blue use 8 bits each, which have integer values from 0 to 255.
# It's important that the training set and the testing set are preprocessed in the same way:

train_images = train_images / 255.0  # reduction  en noir et blanc des images

test_images = test_images / 255.0  # reduction  en noir et blanc des images

# Display the first 25 images from the training set and display the class name below each image.
# Verify that the data is in the correct format and we're ready to build and train the network.

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
# plt.show()


def train_model():
    # Create checkpoint callback
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_weights_only=True,
                                                     verbose=1)
    model.fit(train_images, train_labels, epochs=5, callbacks=[cp_callback])

    return model


def create_model():
    ###
    # Building the neural network requires *configuring the layers of the model*, then *compiling* the model.
    ###

    # The basic building block of a neural network is the layer. Layers extract representations from the data fed into them. And, hopefully, these representations are more meaningful for the problem at hand.

    # Most of deep learning consists of chaining together simple layers.
    # Most layers, like tf.keras.layers.Dense, have parameters that are learned during training.

    model = keras.Sequential([
        # The first layer in this network, tf.keras.layers.Flatten, transforms the format of the images from a 2d-array (of 28 by 28 pixels),to a 1d-array of 28 * 28 = 784 pixels
        keras.layers.Flatten(input_shape=(28, 28)),
        # After the pixels are flattened, the network consists of a sequence of two tf.keras.layers.Dense layers. These are densely-connected, or fully-connected, neural layers.
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    # The first Dense layer has 128 nodes(or neurons).
    # The second(and last) layer is a 10-node softmax layer—this returns an array of 10 probability scores that sum to 1.
    # Each node contains a score that indicates the probability that the current image belongs to one of the 10 classes.

    ###
    # Compile the modèle
    ###

    # - categorical_crossentropy : Loss function —This measures how accurate the model is during training. We want to minimize this function to "steer" the model in the right direction.
    # - Adam: Optimizer —This is how the model is updated based on the data it sees and its loss function.
    # - use for display Metrics —Used to monitor the training and testing steps. The following example uses accuracy, the fraction of the images that are correctly classified.
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


model = create_model()
model.summary()

# If Exist latest checkpoint
model.load_weights(checkpoint_path)

#     Train the model
#     ###

#     # Create checkpoint callback
# cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
#                                                     save_weights_only=True,
#                                                     verbose=1)

# model.fit(train_images, train_labels, epochs=5, callbacks=[cp_callback])


###
# Evaluate the model
###

# Next, compare how the model performs on the test dataset:

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)
print("Untrained model, accuracy: {:5.2f}%".format(100*test_acc))
print('Test loss:', test_loss)


###
# Make Predictions
###

# print(test_images[-1])

# With the model trained, we can use it to make predictions about some images.
predictions = model.predict(test_images)  # By test image

#  Let's take a look at the first prediction:
# print(len(predictions))
# print(len(predictions))


# A prediction is an array of 10 numbers.
#  These describe the "confidence" of the model that the image corresponds to each of the 10 different articles of clothing.
#   We can see which label has the highest confidence value:

print(np.argmax(predictions[1]))

# So the model is most confident that this image is an ankle boot, or class_names[9].
# And we can check the test label to see this is correct:
print(test_labels[1])

# We can graph this to look at the full set of 10 channels


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100*np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#fff716")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('green')


# Let's look at the 0th image, predictions, and prediction array.

i = 0
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions,  test_labels)
# plt.show()

i = 12
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions,  test_labels)
# plt.show()


i = 14
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions,  test_labels)
# plt.show()


i = 18
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions,  test_labels)
# plt.show()


# Let's plot several images with their predictions. Correct prediction labels are blue and incorrect prediction labels are red. The number gives the percent(out of 100) for the predicted label. Note that it can be wrong even when very confident.
