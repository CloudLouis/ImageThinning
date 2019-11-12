import numpy as np
import basic_global_tresholding as bs

thinning_pattern = {
    "b1": {
        "yes": [[0, 0], [0, -1], [-1, -1], [1, -1]],
        "no": [[-1, 1], [0, 1], [1, 1]]
    },
    "b2": {
        "yes": [[0, 0], [-1, 0], [-1, -1], [0, -1]],
        "no": [[0, 1], [1, 1], [1, 0]]
    },
    "b3": {
        "yes": [[0, 0], [-1, 0], [-1, 1], [-1, -1]],
        "no": [[1, -1], [1, 0], [1, 1]]
    },
    "b4": {
        "yes": [[0, 0], [-1, 0], [-1, 1], [0, 1]],
        "no": [[0, -1], [1, 0], [1, -1]]
    },
    "b5": {
        "yes": [[0, 0], [0, 1], [-1, 1], [1, 1]],
        "no": [[-1, -1], [0, -1], [1, -1]]
    },
    "b6": {
        "yes": [[0, 0], [0, 1], [1, 1], [1, 0]],
        "no": [[-1, 0], [-1, -1], [0, -1]]
    },
    "b7": {
        "yes": [[0, 0], [1, 0], [1, 1], [1, -1]],
        "no": [[-1, 1], [-1, 0], [-1, 1]]
    },
    "b8": {
        "yes": [[0, 0], [1, 0], [1, -1], [0, -1]],
        "no": [[-1, 1], [0, 1], [-1, 0]]
    },

}


def read_image_to_hex(image):
    x = open(image, 'rb+')  # read original file to be modified, as byte
    content = x.read().hex()  # convert read file format from byte to hex
    hex_list = []
    for x in range(0, len(content), 2):
        hex_list.append("0x" + content[x] + content[x + 1])
    return hex_list


def thinning(img):
    working = True
    while working:
        print(working)
        old_img_values = np.where(img == 0)
        object_in_img = list(zip(old_img_values[0], old_img_values[1]))
        for t in thinning_pattern:
            for i in object_in_img:
                status = True
                for y in thinning_pattern[t]['yes']:
                    index_x = i[0] + y[0]
                    index_y = i[1] + y[1]
                    try:
                        if index_x >= 0 and index_y >= 0:
                            if img[index_x, index_y] == 255:
                                status = False
                                break
                    except IndexError:
                        pass
                for n in thinning_pattern[t]['no']:
                    index_x = i[0] + n[0]
                    index_y = i[1] + n[1]
                    try:
                        if index_x >= 0 and index_y >= 0:
                            if img[index_x, index_y] == 0:
                                status = False
                                break
                    except IndexError:
                        pass
                if status:
                    img[i[0], i[1]] = 255
        new_img_values = np.where(img == 0)
        if len(old_img_values[0]) == len(new_img_values[0]):
            working = False
    return img


if __name__=="__main__":
    img = bs.read_image_with_global_treshold("finger.pgm")
    img = np.asarray(img, dtype=np.int)
    img = img.reshape((958, 798))

    threshold_img = open("treshold_img.pgm", 'w+', encoding='utf-8')
    header = "P2\n798 958\n255\n"
    threshold_img_value = '\n'.join(str(item) for in_list in img for item in in_list)
    threshold_img.write(header+threshold_img_value)

    result_img = open("result_img.pgm", 'w+', encoding='utf-8')
    img = thinning(img)
    header = "P2\n798 958\n255\n"
    img = '\n'.join(str(item) for in_list in img for item in in_list)
    result_img.write(header+img)
