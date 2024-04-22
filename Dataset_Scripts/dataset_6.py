from time import perf_counter as pc
import matplotlib.pyplot as plt
from matplotlib import patches
import dataset_utils as du
from variables import *
import numpy as np
import matplotlib
import csv
import os

matplotlib.use('QtAgg')


# Dataset 6
# Squares Cut and Circles Cut

squares_folder_train = 'Datasets/Dataset_6/train/squares_cut'
squares_folder_test = 'Datasets/Dataset_6/test/squares_cut'

circles_folder_train = 'Datasets/Dataset_6/train/circles_cut'
circles_folder_test = 'Datasets/Dataset_6/test/circles_cut'

data_folder = 'Datasets/Dataset_6/data'
seed = 390
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)
os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()
squares_writer = csv.writer(open(os.path.join(data_folder, 'squares_cut.csv'), 'w'))
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

circles_writer = csv.writer(open(os.path.join(data_folder, 'circles_cut.csv'), 'w'))
circles_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Cut', 'Variant'])

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
        area = length ** 2
        visible_area = du.calculate_visible_area_square(x, y, length, angle, img_width, img_height)
        dfc = du.calculate_dfc_square(x, y, length, angle, img_width, img_height)
        dfc = round(dfc, 2)
        area = round(area, 2)
        visible_area = round(visible_area, 2)
        squares_writer.writerow([f'square_cut_{counter}.png', x, y, length, angle, area, visible_area, color, bg_color, dfc, corners, "True", variant])
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
        path = os.path.join(folder, f'square_cut_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1

# Circles Cut
print("\r", flush=True)
counter = 1
for j in range(2):
    print("\n")
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_circle_area, max_circle_area, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='equal')
        b = f"Generating Circles {i+1}/{size}"
        print(b, end='\r', flush=True)
        all_ok = False
        tries = 0
        max_tries = 10
        while all_ok is False:
            if tries >= max_tries:
                radius = np.random.uniform(min_circle_area, max_circle_area)
                radius = np.sqrt(radius/np.pi)
                tries = 0
            else:
                radius = np.sqrt(distribution[i]/np.pi)
            x = np.random.uniform(0-radius+outside_min, img_width + radius - outside_min)
            y = np.random.uniform(0-radius+outside_min, img_height + radius - outside_min)

            if du.circle_is_cut(x, y, radius, img_width, img_height) is False:
                tries += 1
                continue

            all_ok = True

        bg_color = du.generate_nonmatching_color()
        color = du.generate_nonmatching_color(bg_color)
        area = np.pi * radius ** 2
        visible_area = du.calculate_visible_area_circle(x, y, radius, img_width, img_height)
        dfc = du.calculate_dfc_circle(x, y, radius, img_width, img_height)
        dfc = round(dfc, 2)
        area = round(area, 2)
        visible_area = round(visible_area, 2)
        circles_writer.writerow([f'circle_cut_{counter}.png', x, y, radius, area, visible_area, color, bg_color, dfc, "True", variant])
        fig.set_facecolor(bg_color)
        circle = patches.Circle((x, y), radius, color=color)
        ax.add_patch(circle)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = circles_folder_train
        else:
            folder = circles_folder_test
        path = os.path.join(folder, f'circle_cut_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1
end = pc()
print(f"Finished generating images ({round(end - start, 4)}s)")
