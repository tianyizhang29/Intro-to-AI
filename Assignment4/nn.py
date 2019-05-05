import numpy as np
import time
from PIL import Image
from pylab import *
import json

def init_three_layer(input_size, h1_size, h2_size, output_size):
    model = {}
    model['W1'] = 0.01 * np.random.randn(input_size, h1_size)
    model['b1'] = np.zeros(h1_size)
    model['W2'] = 0.01 * np.random.randn(h1_size, h2_size)
    model['b2'] = np.zeros(h2_size)
    model['W3'] = 0.01 * np.random.randn(h2_size, output_size)
    model['b3'] = np.zeros(output_size)
    return model

def NN(model, X, y, batch_size):
    W1, b1, W2, b2, W3, b3= model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
    step_size = 0.01
    reg = 1e-3
    loss = -1
    for j in range(batch_size):
        hidden1 = np.maximum(0, np.dot(X, W1) + b1)  #ReLU
        hidden2 = np.maximum(0, np.dot(hidden1, W2) + b2) #ReLU
        scores = np.dot(hidden2, W3) + b3

        exp_scores = np.exp(scores)
        # probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        sigmoid = exp_scores / (1 + exp_scores)
        probs = 255 * sigmoid

        loss = np.sqrt(sum(abs(y - probs)) ** 2)

        # correct_logprobs = -np.log(probs[range(num_example), y])
        # data_loss = np.sum(correct_logprobs) / num_example
        # reg_loss = 0.5*reg*np.sum(W1*W1) + 0.5*reg*np.sum(W2*W2) + 0.5*reg*np.sum(W3*W3)
        # loss = data_loss + reg_loss

        dscores = 255 * sigmoid * (1 - sigmoid)
        dscores /= batch_size

        # backprop
        dW3 = np.dot(hidden2.T, dscores)
        db3 = np.sum(dscores, axis=0, keepdims=True)
        # next into hidden2 layer
        dhidden2 = np.dot(dscores, W3.T)
        dhidden2[hidden2 <= 0] = 0

        dW2 = np.dot(hidden1.T, dhidden2)
        db2 = np.sum(dhidden2, axis=0, keepdims=True)

        dhidden1 = np.dot(dhidden2, W2.T)
        dhidden1[hidden1 <= 0] = 0

        dW1 = np.dot(X.T, dhidden1)
        db1 = np.sum(dhidden1, axis=0, keepdims=True)

        dW3 += reg * W3
        dW2 += reg * W2
        dW1 += reg * W1

        W1 += -step_size * dW1
        W2 += -step_size * dW2
        W3 += -step_size * dW3
        b1 = b1 + -step_size * db1
        b2 = b2 + -step_size * db2
        b3 = b3 + -step_size * db3
        print("iteration %d: loss %f" % (j, loss))

    print("Epoch %d finished" % (i))
    model = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2, 'W3': W3, 'b3': b3}
    return model


def predict(model, test):
    W1, b1, W2, b2, W3, b3= model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
    hidden1 = np.maximum(0, np.dot(test, W1) + b1)  #ReLU
    hidden2 = np.maximum(0, np.dot(hidden1, W2) + b2) #ReLU
    scores = np.dot(hidden2, W3) + b3

    exp_scores = np.exp(scores)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs, axis=1)

def load_img():
    img_size = 120
    gray_data = []
    origin_batch_data = []

    for i in range(1, img_size + 1):
        im = array(Image.open('./data/' + str(i) + '.jpg'))
        im_gray = copy(im)
        r = im[:,:,0]
        g = im[:,:,1]
        b = im[:,:,2]
        gray = 0.21*r + 0.72*g + 0.07*b
        im_gray[:,:,0] = gray
        im_gray[:,:,1] = gray
        im_gray[:,:,2] = gray
        im_gray = np.shape([3 * 236 * 236])
        gray_data.append(im_gray)
        origin_batch_data.append(im)

    return origin_batch_data, gray_data

def train():
    model = init_three_layer(256 * 256 * 3, 256 * 256 * 3, 256 * 256 * 3, 256 * 256 * 3)
    batch_size = 120
    epoch = 100
    origin_batch_data, batch_data = load_img()
    for i in range(epoch):
        model = NN(model, batch_data, origin_batch_data, batch_size)

    filename = 'model_data'
    with open(filename+'.json','a') as outfile:
        json.dump(model, outfile,ensure_ascii=False)
        outfile.write('\n')

    # outputlabels = predict(model, gray_data)
    # result = y_test - outputlabels
    # result = (1 - np.count_nonzero(result)/len(outputlabels))
    # print ("---Accuracy for nn on mnist: %s ---" %result)
    # print ("---execution time: %s seconds ---" % (time.time() - start_time))

train()