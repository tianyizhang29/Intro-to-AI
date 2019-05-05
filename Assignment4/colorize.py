import keras
# import tensorflow as tf
from skimage.io import imread, imsave
from skimage.color import rgb2gray, gray2rgb, rgb2lab, lab2rgb
from keras.preprocessing.image import img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose
import numpy as np
from conv2d import *


def image_color_test():
    test_image_gray = rgb2gray(imread('data/tree.jpg'))
    test_image_rgb = imread('data/tree.jpg')

    print(test_image_gray.shape)
    print(test_image_gray)
    print(test_image_rgb.shape)

def reshapePic(pic):
    return pic.reshape((256,256,3))

def get_train_data(img_file):
    image = img_to_array(load_img(img_file))
    image_shape = image.shape
    image = np.array(image, dtype=float)

    x = rgb2lab(1.0 / 255 * image)[:, :, 0]
    y = rgb2lab(1.0 / 255 * image)[:, :, 1:]
    x1 = rgb2lab(image)[:, :, 0]
    y1 = rgb2lab(image)[:, :, 1:]
    # x = x.reshape(1, image_shape[0], image_shape[1], 1)
    # y = y.reshape(1, image_shape[0], image_shape[1], 2)
    return x, y, image_shape

def initial_model():
    model={}
    model['w1'] = 0.01 * np.random.randn(3, 3)
    model['w2'] = 0.01 * np.random.randn(3, 3)
    model['w3'] = 0.01 * np.random.randn(3, 3)
    model['w4'] = 0.01 * np.random.randn(3, 3)
    model['w5'] = 0.01 * np.random.randn(3, 3)
    model['w6'] = 0.01 * np.random.randn(3, 3)
    model['w7'] = 0.01 * np.random.randn(3, 3)
    model['w8'] = 0.01 * np.random.randn(3, 3)
    model['w91'] = 0.01 * np.random.randn(3, 3)
    model['w92'] = 0.01 * np.random.randn(3, 3)

def train(model, x, y): # x is gray scale image; y is color image
    w1 = model['w1'], w2 = model['w2'], w3 = model['w3'],  w4 = model['w4'], w5 = model['w5'], w6 = model['w6'],
    w7 = model['w7'], w8 = model['w8'], w91 = model['w91'], w92 = model['w92']
    step_size = 0.01
    #forward
    output1, cache1 = conv_forward(x, w1, stride=2)
    output1 = np.maximum(output1, 0) #layer1 relu

    output2, cache2 = conv_forward(output1, w2, stride=1)
    output2 = np.maximum(output2, 0) #layer2 relu

    output3, cache3 = conv_forward(output2, w3, stride=1)
    output3 = np.maximum(output3, 0) #layaer3 relu

    output4, cache4 = conv_forward(output3, w4, stride=2)
    output4 = np.maximum(output4, 0) #layer4 relu

    output5, cache5 = conv_forward(output4, w5, stride=1)
    output5 = np.maximum(output5, 0) #layer5 relu

    output6, cache6 = conv_forward(output5, w6, stride=2)
    output6 = np.maximum(output6, 0) #layer6 relu

    output_up1 = upsampling2d_forward(output6, (2,2)) #upsampling layer1

    output7, cache7 = conv_forward(output_up1, w7, stride=1)
    output7 = np.maximum(output7, 0) #layer7 relu

    output_up2 = upsampling2d_forward(output7, (2,2)) #upsampling layer2

    output8, cache8 = conv_forward(output_up2, w8, stride=1)
    output8 = np.maximum(output8, 0) #layer7 relu

    output_up3 = upsampling2d_forward(output8, (2,2)) #upsampling layer8

    output91, cache91 = conv_forward(output_up3, w91)
    output92, cache92 = conv_forward(output_up3, w92)
    output9 = np.zeros((256,256,2))
    output9[:, :, 0] = output91
    output9[:, :, 1] = output92 #outputlayer 9

    # 128 * sigmoid
    exp_scores = np.exp(output9)
    sigmoid = exp_scores / (1 + exp_scores)
    res = 128 * sigmoid

    loss = np.sqrt(np.sum((y[:,:,0:2] - res)**2))

    #backward
    dres = 128 * sigmoid * (1 - sigmoid)
    dX91, dW91 = conv_backward(dres[:, :, 0], cache91)
    dX92, dW92 = conv_backward(dres[:, :, 1], cache92)
    dW9 = dW91 + dW92
    dX9 = dX91 + dX92
    dW9_down = upsampling2d_backward(dW9, (2,2))
    dX9_down = upsampling2d_backward(dX9, (2,2))
    dW8, dW8 = conv_backward(dX9_down, cache8)


if __name__ == '__main__':
    get_train_data('data/1.jpg')