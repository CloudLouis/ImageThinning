import pandas as pd
import io
import matplotlib.pyplot as plt


def read_image_with_global_treshold(image):
    hex_list = read_image_to_hex(image)

    hist = count_intensity(hex_list)  # get frequency of every intensity
    t = int((len(hist)-1)/2)
    while True:  # update threshold value until it stays the same
        n_t = treshold(t, hist)  # calculate new threshold
        if t == n_t:
            break
        else:
            t = n_t
    return create_new_image(hex_list, t)  # apply threshold to image


def treshold(initial, hist):  # function to update threshold value
    x = 0
    temp_x = 0
    y = 0
    temp_y = 0
    for i in range(0, initial+1):
        # print(i)
        x += i*hist[i]
        temp_x += hist[i]
    x = x/temp_x
    for i in range(initial+1, len(hist)):
        # print(i)
        y += i*hist[i]
        temp_y += hist[i]
    y = y/temp_y
    return int((x+y)/2)


def read_image_to_hex(image):
    x = open(image, 'rb+')  # read original file to be modified, as byte
    content = x.read().hex()    # convert read file format from byte to hex
    hex_list = []
    for x in range(0, len(content), 2):
        hex_list.append("0x"+content[x]+content[x+1])
    return hex_list


def count_intensity(hex_list):  # get frequency for every intensity
    histogram_table = {}
    for h in range(0, 256):
        histogram_table[h] = 0

    for h in range(0, len(hex_list)):
        if h > 14:  # skip the header of
            # grab the value of the current pixel and make a count of each pixel
            pixel = int(hex_list[h], 0)
            histogram_table[pixel] += 1
    return histogram_table


def create_new_image(hex_list, treshold):  # apply treshold to image
    header = []  # header for new file, P2 type, same size, 255 max value
    for h in range(0, len(hex_list)):
        if h > 14:  # skip the header of current image
            x = int(hex_list[h], 0)
            if x <= treshold:
                header.append(0)
            else:
                header.append(255)
    return header
