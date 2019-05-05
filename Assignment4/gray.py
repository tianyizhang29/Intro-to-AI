from PIL import Image
from pylab import *

im = array(Image.open('./data/1.jpg'))
im_gray = copy(im)
r = im[:,:,0]
g = im[:,:,1]
b = im[:,:,2]
gray = 0.21*r + 0.72*g + 0.07*b
im_gray[:,:,0] = gray
im_gray[:,:,1] = gray
im_gray[:,:,2] = gray

# subplot(121)
# title('color')
# imshow(im)
# subplot(122)
# title('gray')
# imshow(im_gray)
# show()
# im_gray = Image.fromarray(im_gray)
# im_gray.save('./data/gray_1.jpg')