from PIL import Image
from pylab import *
from math import *
import csv
import pandas as pd



class mapping_color:
    img_size = 256
    def __init__(self, color_board):
        self.img_size = 256
        self. color_board = color_board

    def encode_color(self, color):
        return color[0] * 1000 * 1000 + color[1] * 1000 + color[2]

    def decode_color(self, color_value):
        color = []
        color.append(color_value % 1000)
        color_value //= 1000
        color.append(color_value % 1000)
        color_value //= 1000
        color.append(color_value % 1000)
        color = color[::-1]
        return color

    def load_img(self,path):
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


    def load_imgs(self, path):
        color_imgs, gray_imgs = [], []
        for i in range(1, 51):
            color_img, gray_img = self.load_img(path + '/' + str(i) + '.jpg')
            color_imgs.append(color_img)
            gray_imgs.append(gray_img)
        return color_imgs, gray_imgs


    def color_distance(self, color1, color2):
        return (color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2


    def find_nearest_color(self, color):
        min_dis = 200000
        min_color = []
        for i in range(len(self.color_board)):
            dis = self.color_distance(color, self.color_board[i])
            if dis < min_dis:
                min_color = self.color_board[i]
                min_dis = dis
        # print(min_color)
        return min_color


    def learn_img(self, gray_to_color, color_img, gray_img):
        for i in range(self.img_size):
            for j in range(self.img_size):
                pixel_gray = gray_img[i][j][0]
                pixel_color = color_img[i][j]
                nearest_color = self.find_nearest_color(pixel_color)
                nearest_color_value = self.encode_color(nearest_color)
                pixel_gray_dict = gray_to_color[pixel_gray]
                if nearest_color_value in pixel_gray_dict:
                    pixel_gray_dict[nearest_color_value] += 1
                else:
                    pixel_gray_dict[nearest_color_value] = 1

    def find_max_color(self, gray_to_color):
        mapping = {}
        for i in range(256):
            color_to_times = gray_to_color[i]
            max_value = 0
            max_color = 0
            for key in color_to_times:
                if color_to_times[key] > max_value:
                    max_value = color_to_times[key]
                    max_color = key
            mapping[i] = self.decode_color(max_color)
        return mapping

    def find_avg_color(self, gray_to_color):
        mapping = {}
        for i in range(256):
            color_to_times = gray_to_color[i]
            if not bool(color_to_times):
                mapping[i] = [255,255,255]
                continue
            sum1 = 0
            sum2 = 0
            sum3 = 0
            times_sum = 0
            for key in color_to_times:
                encode_color = key
                rbg_color = self.decode_color(encode_color)
                sum1 += key * rbg_color[0]
                sum2 += key * rbg_color[1]
                sum3 += key * rbg_color[2]
                times_sum += color_to_times[key]
            r_color = sum1 // times_sum
            g_color = sum2 // times_sum
            b_color = sum3 // times_sum
            mapping[i] = [r_color, g_color, b_color]
        return mapping


    def mapping_gray_color(self, path):
        color_imgs, gray_imgs = self.load_imgs(path)
        img_num = len(color_imgs)
        gray_to_color = {}

        for i in range(256):
            gray_to_color[i] = {}

        for i in range(img_num):
            self.learn_img(gray_to_color, color_imgs[i], gray_imgs[i])
            print("Finished learning Image {}".format(i))

        mapping = self.find_max_color(gray_to_color)
        return mapping

    def colorize(self, gray, mapping):
        color = np.zeros((256, 256, 3), dtype=uint8)

        for i in range(len(gray)):
            for j in range(len(gray[0])):
                gray_pixel = gray[i][j][0]
                if gray_pixel in mapping:
                   color[i][j] = mapping[gray_pixel]
                else:
                    color[i][j] = [255,255,255]
        return color

    def save_csv(self, data, filename):
        with open(filename,"w",newline="") as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["gray_value","rgb_value"])
            for key in data:
                writer.writerows([[key, data[key]]])
        close()

    def load_csv(self, filename):
        map = {}
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for item in reader:
                map[item[reader.fieldnames[0]]] = item[reader.fieldnames[1]]
        return map

if __name__ == '__main__':
    # # color_board = [[34,140,226], [76, 127, 32], [36, 66, 4], [108, 159, 4], [106, 162, 2],
    # #                [67, 125, 38], [87, 115, 49], [0, 200, 202], [5, 124, 156], [23, 113, 150],
    # #                [38, 127, 227], [255, 255, 255], [167, 196, 228], [250, 247, 230],[249, 249, 232],
    # #                [253, 249, 227], [221, 162, 62], [183, 167, 152], [90, 109, 116]]
    color_board = [(109, 142, 32), (45, 107, 172), (64, 89, 22), (77, 136, 154),
                   (56, 67, 27), (156, 152, 113), (70, 105, 9), (111, 131, 135),
                   (50, 135, 15), (64, 137, 129), (73, 130, 7), (31, 91, 126),
                   (131, 121, 36), (10, 67, 2), (108, 105, 67), (103, 184, 234),
                   (83, 145, 73), (26, 42, 3), (130, 144, 10), (30, 45, 26), (20, 143, 164),
                   (82, 142, 25), (78, 174, 175), (222, 212, 179), (126, 181, 201),
                   (43, 85, 78), (31, 125, 224), (112, 127, 94), (6, 51, 47)]
    mapping = mapping_color(color_board)
    map = mapping.mapping_gray_color('./data')
    _, gray = mapping.load_img('./data/62.jpg')
    # mapping = {1:[2,3,4]}
    # mapping.save_csv(map, "test1")

    # mapping = load_csv()
    res = mapping.colorize(gray, map)

    # res = [[[1,1,1]]]
    res = Image.fromarray(res)
    imshow(res)
    show()
    # encode = mapping.encode_color((109, 142, 32))
    # decode = mapping.decode_color(encode)
    # print(decode)
