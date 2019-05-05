"""
this file is the simple version of colorize
you are going to need skimage and keras for it
any version should be compatible
"""
import keras
import tensorflow as tf
from skimage.io import imread, imsave
from skimage.color import rgb2gray, gray2rgb, rgb2lab, lab2rgb
from keras.models import Sequential
from keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import os


def get_train_data(img_file):
    image = img_to_array(load_img(img_file))
    image_shape = image.shape
    image = np.array(image, dtype=float)

    x = rgb2lab(1.0 / 255 * image)[:, :, 0]
    y = rgb2lab(1.0 / 255 * image)[:, :, 1:]
    y /= 128
    x = x.reshape(1, image_shape[0], image_shape[1], 1)
    y = y.reshape(1, image_shape[0], image_shape[1], 2)
    return x, y, image_shape


def build_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(None, None, 1)))
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same', strides=2)) #1
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same')) #2
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same')) #3
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same', strides=2)) #4
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same')) #5
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same', strides=2)) #6
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same')) #7
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(1, (3, 3), activation='relu', padding='same')) #8
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(2, (3, 3), activation='tanh', padding='same')) #9
    model.compile(optimizer='rmsprop', loss='mse')
    return model


def train():
    model = build_model()

    num_epochs = 6000
    batch_size = 6
    model_file = '128model.h5'
    for i in range(1, 25):
        x, y, img_shape = get_train_data('./data/'+ str(i) +'.jpg')
        model.fit(x, y, batch_size=16, epochs=100)
    model.save(model_file)

def colorize():
    x, y, image_shape = get_train_data('./data/100.jpg')
    model = build_model()
    model.load_weights('128model.h5')
    output = model.predict(x)
    output *= 128
    tmp = np.zeros((256, 256, 3))
    tmp[:, :, 0] = x[0][:, :, 0]
    tmp[:, :, 1:] = output[0]
    imsave("100_.png", lab2rgb(tmp))
    imsave("100_gray.png", rgb2gray(lab2rgb(tmp)))

if __name__ == '__main__':
    # train()
    colorize()