from PIL import Image
from pylab import *
from math import *
import csv
import pandas as pd

img_size = 256
color_board = [[34,140,226], [76, 127, 32], [36, 66, 4], [108, 159, 4], [106, 162, 2],
               [67, 125, 38], [87, 115, 49], [0, 200, 202], [5, 124, 156], [23, 113, 150],
               [38, 127, 227], [255, 255, 255], [167, 196, 228], [250, 247, 230],[249, 249, 232],
               [253, 249, 227], [221, 162, 62], [183, 167, 152], [90, 109, 116]]

def encode_color(color):
    return color[2] * 1000 * 1000 + color[1] * 1000 + color[0]

def decode_color(color_value):
    color = []
    color.append(color_value % 1000)
    color_value /= 1000
    color.append(color_value % 1000)
    color_value /= 1000
    color.append(color_value % 1000)
    color = color[::-1]
    return color

def load_img(path):
    color_img = array(Image.open(path))
    gray_img = copy(color_img)
    r = color_img[:, :, 0]
    g = color_img[:, :, 1]
    b = color_img[:, :, 2]
    gray = 0.21 * r + 0.72 * g + 0.07 * b
    gray_img[:, :, 0] = gray
    gray_img[:, :, 1] = gray
    gray_img[:, :, 2] = gray
    # subplot(121)
    # title('color')
    # imshow(color_img)
    # subplot(122)
    # title('gray')
    # imshow(gray_img)
    # show()
    # gray_img = Image.fromarray(gray_img)
    # gray_img.save('./data/gray_1.jpg')
    return color_img, gray_img


def load_imgs(path):
    color_imgs, gray_imgs = [], []
    for i in range(1, 21):
        color_img, gray_img = load_img(path + '/' + str(i) + '.jpg')
        color_imgs.append(color_img)
        gray_imgs.append(gray_img)
    return color_imgs, gray_imgs


def color_distance(color1, color2):
    return (color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2


def find_nearest_color(color):
    min_dis = 200000
    min_color = []
    for i in range(len(color_board)):
        dis = color_distance(color, color_board[i])
        if dis < min_dis:
            min_color = color_board[i]
            min_dis = dis
    # print(min_color)
    return min_color


def learn_img(gray_to_color, color_img, gray_img):
    for i in range(img_size):
        for j in range(img_size):
            pixel_gray = gray_img[i][j][0]
            pixel_color = color_img[i][j]
            nearest_color = find_nearest_color(pixel_color)
            nearest_color_value = encode_color(nearest_color)
            pixel_gray_dict = gray_to_color[pixel_gray]
            if nearest_color_value in pixel_gray_dict:
                pixel_gray_dict[nearest_color_value] += 1
            else:
                pixel_gray_dict[nearest_color_value] = 1

def find_max_color(gray_to_color):
    mapping = {}
    for i in range(256):
        color_to_times = gray_to_color[i]
        max_value = 0
        max_color = 0
        for key in color_to_times:
            if color_to_times[key] > max_value:
                max_value = color_to_times[key]
                max_color = key
        mapping[i] = decode_color(max_color)
    return mapping


def mapping_gray_color(path):
    color_imgs, gray_imgs = load_imgs(path)
    img_num = len(color_imgs)
    gray_to_color = {}

    for i in range(256):
        gray_to_color[i] = {}

    for i in range(img_num):
        learn_img(gray_to_color, color_imgs[i], gray_imgs[i])
        print("Finished learning Image {}".format(i))

    mapping = find_max_color(gray_to_color)
    return mapping

def colorize(gray, mapping):
    color = np.zeros((256, 256, 3), dtype=uint8)

    for i in range(len(gray)):
        for j in range(len(gray[0])):
            gray_pixel = gray[i][j][0]
            if gray_pixel in mapping:
               color[i][j] = mapping[gray_pixel]
            else:
                color[i][j] = [255,255,255]
    return color

def save_csv(data):
    with open("test.csv","w") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["gray_value","rgb_value"])
        for key in data:
            writer.writerows([[key, data[key]]])

def load_csv():
    mapping = {}

    csv = pd.read_csv('test.csv')

    # print(csv)
    return mapping

if __name__ == '__main__':
    mapping = mapping_gray_color('./data')
    _, gray = load_img('./data/1.jpg')
    # mapping = {1:[2,3,4]}
    save_csv(mapping)

    # mapping = load_csv()
    res = colorize(gray, mapping)

    # res = [[[1,1,1]]]
    res = Image.fromarray(res)
    imshow(res)
    show()