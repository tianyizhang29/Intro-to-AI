from mapping_color import *
from kmeans import *

def main():
    pic_num = 5
    k = 29
    path = "./data"

    for i in range(1, pic_num + 1):
        if i == 1:
            img = array(Image.open(path + '/1.jpg'))
            datas = img.reshape((-1,3))
        else:
            img = array(Image.open(path + '/' + str(i) + '.jpg'))
            flatten = img.reshape((-1,3))
            datas = np.append(datas, flatten, axis=0)
        print("pic {0} loaded for clustering".format(i))
    km = KMeans(datas)
    km.run(k)
    color_board = km.results # get the cluster location;
    print(color_board)
    mapping = mapping_color(color_board)
    map = mapping.mapping_gray_color(path)
    mapping.save_csv(map, "./model/56.csv")
    _, gray = mapping.load_img('./data/1.jpg')
    res = mapping.colorize(gray, map)
    res = Image.fromarray(res)
    imshow(res)
    show()

if __name__ == '__main__':
    main()