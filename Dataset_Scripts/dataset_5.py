import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patches
import csv
import os
import dataset_utils as du
from variables import *
from time import perf_counter as pc
matplotlib.use('QtAgg')


# Dataset 5
# Squares Cut and Squares

squares_folder_train = 'Datasets/Dataset_5/train/squares'
squares_folder_test = 'Datasets/Dataset_5/test/squares'

squares_cut_folder_train = 'Datasets/Dataset_5/train/squares_cut'
squares_cut_folder_test = 'Datasets/Dataset_5/test/squares_cut'

data_folder = 'Datasets/Dataset_5/data'
seed = 921
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)
os.makedirs(squares_cut_folder_train, exist_ok=True)
os.makedirs(squares_cut_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()
squares_writer = csv.writer(open(os.path.join(data_folder, 'squares.csv'), 'w'))
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

squares_cut_writer = csv.writer(open(os.path.join(data_folder, 'squares_cut.csv'), 'w'))
squares_cut_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

fig = plt.figure(figsize=(img_width/100, img_height/100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Squares Cut
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_area, max_square_area, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='auto')
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        all_ok = False
        tries = 0
        max_tries = 10
        while all_ok is False:
            if tries >= max_tries:
                length = np.random.uniform(min_square_area, max_square_area)
                length = np.sqrt(length)
                tries = 0
            else:
                length = np.sqrt(distribution[i])
            angle = np.random.uniform(0, 360)
            x = np.random.uniform(0 - length + outside_min, img_width + length - outside_min)
            y = np.random.uniform(0 - length + outside_min, img_height + length - outside_min)
            center_x = x + length / 2
            center_y = y + length / 2
            square = patches.Rectangle((x, y), length, length, angle=angle, rotation_point=(center_x, center_y))
            corners = square.get_corners()

            if du.square_is_cut(corners, img_width, img_height) is False:
                tries += 1
                continue
            all_ok = True

        bg_color = du.generate_nonmatching_color()
        color = du.generate_nonmatching_color(bg_color)
        area = round(length ** 2, 2)
        visible_area = du.calculate_visible_area_square(x, y, angle, length, img_width, img_height)
        dfc = du.calculate_dfc_square(x, y, length, angle, img_width, img_height)
        dfc = round(dfc, 2)
        area = round(area, 2)
        visible_area = round(visible_area, 2)
        squares_cut_writer.writerow([f'square_cut_{counter}.png', x, y, length, angle, area, visible_area, color, bg_color, dfc, corners, "True", variant])
        fig.set_facecolor(bg_color)
        square.set_color(color)
        ax.add_patch(square)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = squares_cut_folder_train
        else:
            folder = squares_cut_folder_test
        path = os.path.join(folder, f'square_cut_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1

# Squares
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_area, max_square_area, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='auto')
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        all_ok = False
        tries = 0
        max_tries = 10
        while all_ok is False:
            if tries >= max_tries:
                length = np.random.uniform(min_square_area, max_square_area)
                length = np.sqrt(length)
                tries = 0
            else:
                length = np.sqrt(distribution[i])
            angle = np.random.uniform(0, 360)
            x = np.random.uniform(0, img_width - length)
            y = np.random.uniform(0, img_height - length)
            center_x = x + length / 2
            center_y = y + length / 2
            square = patches.Rectangle((x, y), length, length, angle=angle, rotation_point=(center_x, center_y))
            corners = square.get_corners()

            if du.square_out_of_bounds(corners, img_width, img_height):
                tries += 1
                continue
            all_ok = True

        bg_color = du.generate_nonmatching_color()
        color = du.generate_nonmatching_color(bg_color)
        area = length ** 2
        dfc = du.calculate_dfc_square(x, y, length, angle, img_width, img_height)
        dfc = round(dfc, 2)
        area = round(area, 2)
        squares_writer.writerow([f'square_{counter}.png', x, y, length, angle, area, color, bg_color, dfc, corners, "False", variant])
        fig.set_facecolor(bg_color)
        square.set_color(color)
        ax.add_patch(square)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = squares_folder_train
        else:
            folder = squares_folder_test
        path = os.path.join(folder, f'square_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1
