import numpy as np

def conv_forward(X, W, stride=1):
    '''
    The forward computation for a convolution function

    Arguments:
    X -- output activations of the previous layer, numpy array of shape (n_H_prev, n_W_prev) assuming input channels = 1
    W -- Weights, numpy array of size (f, f) assuming number of filters = 1

    Returns:
    H -- conv output, numpy array of size (n_H, n_W)
    cache -- cache of values needed for conv_backward() function
    '''

    # Retrieving dimensions from X's shape
    (n_H_prev, n_W_prev) = X.shape

    # Retrieving dimensions from W's shape
    (f, f) = W.shape

    assert (n_H_prev - f) % stride == 0
    assert (n_W_prev - f) % stride == 0

    # Compute the output dimensions assuming no padding and stride = 1
    n_H = int(n_H_prev - f) // stride + 1
    n_W = int(n_W_prev - f) // stride + 1

    # Initialize the output H with zeros
    H = np.zeros((n_H, n_W))
    n_h = 0
    n_w = 0
    # Looping over vertical(h) and horizontal(w) axis of output volume
    for h in range(0, n_H):
        for w in range(0, n_W):
            x_slice = X[stride*h:stride*h+f, stride*w:stride*w+f]
            H[n_h,n_w] = np.sum(x_slice * W)
            n_w += 1
        n_h += 1
        n_w = 0
    # Saving information in 'cache' for backprop
    cache = (X, W)

    return H, cache

def conv_backward(dH, cache, stride=1):
    '''
    The backward computation for a convolution function

    Arguments:
    dH -- gradient of the cost with respect to output of the conv layer (H), numpy array of shape (n_H, n_W) assuming channels = 1
    cache -- cache of values needed for the conv_backward(), output of conv_forward()

    Returns:
    dX -- gradient of the cost with respect to input of the conv layer (X), numpy array of shape (n_H_prev, n_W_prev) assuming channels = 1
    dW -- gradient of the cost with respect to the weights of the conv layer (W), numpy array of shape (f,f) assuming single filter
    '''

    # Retrieving information from the "cache"
    (X, W) = cache

    # Retrieving dimensions from X's shape
    (n_H_prev, n_W_prev) = X.shape

    # Retrieving dimensions from W's shape
    (f, f) = W.shape

    # Retrieving dimensions from dH's shape
    (n_H, n_W) = dH.shape

    # Initializing dX, dW with the correct shapes
    dX = np.zeros(X.shape)
    dW = np.zeros(W.shape)

    # Looping over vertical(h) and horizontal(w) axis of the output
    for h in range(n_H):
        for w in range(n_W):
            dX[stride*h:stride*h+f, stride*w:stride*w+f] += W * dH[h,w]
            dW += X[stride*h:stride*h+f, stride*w:stride*w+f] * dH[h,w]

    return dX, dW

def upsampling2d_forward(X, W):
    # H is the output after upsampling

    (length, width) = W
    (n_H_prev, n_W_prev) = X.shape
    n_H = n_H_prev * length
    n_W = n_W_prev * width
    H = np.zeros((n_H, n_W))

    for h in range(0, n_H_prev):
        for w in range(0, n_W_prev):
            H[h*2:h*2+2, w*2:w*2+2] = X[h,w]
    return H

def upsampling2d_backward(X, W):
    # H is the output after upsampling

    (length, width) = W
    (n_H_prev, n_W_prev) = X.shape

    assert n_H_prev % length == 0
    assert n_W_prev % width == 0

    n_H = n_H_prev // length
    n_W = n_W_prev // width
    H = np.zeros((n_H, n_W))

    for h in range(0, n_H_prev, length):
        for w in range(0, n_W_prev, width):
            H[h//2, w//2] = X[h,w]
    return H

if __name__ == '__main__':
    X = np.array([[1,0,0,0,1],
                  [-1,0,2,1,2],
                  [1,0,-2,0,-1],
                  [1,1,0,0,2],
                  [-2,0,3,0,0]])
    w = np.array([[1,0,2],
                  [-1,1,1],
                  [0,2,1]])
    # H, cache = conv_forward(X,w,1)
    # dX, dW = conv_backward(np.array([[1,1,1],
    #                                 [1,1,1],
    #                                 [1,1,1]]), cache)
    H = upsampling2d_forward(w, (2,2))
    print(H)
    H = upsampling2d_backward(H, (2,2))
    print(H)
