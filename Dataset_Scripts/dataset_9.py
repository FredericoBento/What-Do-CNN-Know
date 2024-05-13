import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
import csv
import os
from time import perf_counter as pc
import dataset_utils as du
from variables import *

matplotlib.use('QtAgg')


# Dataset 9 Circles, Squares, Nones

circles_folder_train = 'Datasets/Dataset_9/train/circles'
circles_folder_test = 'Datasets/Dataset_9/test/circles'

squares_folder_train = 'Datasets/Dataset_9/train/squares'
squares_folder_test = 'Datasets/Dataset_9/test/squares'

nones_folder_train = 'Datasets/Dataset_9/train/nones'
nones_folder_test = 'Datasets/Dataset_9/test/nones'

data_folder = 'Datasets/Dataset_9/data'
seed = 442
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)

os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)

os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)

os.makedirs(nones_folder_train, exist_ok=True)
os.makedirs(nones_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()
ci_writer = csv.writer(open(os.path.join(data_folder, 'circles.csv'), 'w'))
ci_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Distance From Center', 'Distance From Center Further', 'Color', 'Bg_color', 'Variant'])

sq_writer = csv.writer(open(os.path.join(data_folder, 'squares.csv'), 'w'))
sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Distance From Center', 'Distance From Center Further', 'Corners', 'Color', 'Bg_color', 'Variant'])

nones_writer = csv.writer(open(os.path.join(data_folder, 'nones.csv'), 'w'))
nones_writer.writerow(['Filename', 'Color', 'Bg_color', 'Variant'])

fig = plt.figure(figsize=(img_width / 100, img_height / 100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_circle_area, max_circle_area, size)

    for i in range(size):
        b = f"Generating Circles {i+1}/{size} "
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111, aspect='equal')
        bg_color = du.generate_nonmatching_color()
        exclude_colors = [bg_color]

        ci_area = distribution[i]
        ci_radius = np.sqrt(ci_area / np.pi)
        ci_x = np.random.uniform(0 + ci_radius, img_width - ci_radius)
        ci_y = np.random.uniform(0 + ci_radius, img_height - ci_radius)

        while du.circle_out_of_bounds(ci_x, ci_y, ci_radius, img_width, img_height):
            ci_x = np.random.uniform(0 + ci_radius, img_width - ci_radius)
            ci_y = np.random.uniform(0 + ci_radius, img_height - ci_radius)

        ci_dfc = du.calculate_dfc_circle(ci_x, ci_y, ci_radius, img_width, img_height)
        ci_dfc_f = du.calculate_dfc_further_circle(ci_x, ci_y, ci_radius, img_width, img_height)
        ci_color = du.generate_nonmatching_color()
        exclude_colors.append(ci_color)

        ax.add_patch(patches.Circle((ci_x, ci_y), ci_radius, color=ci_color))

        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        filename = f'circles_{counter}.png'
        if j == 0:
            fig.savefig(os.path.join(circles_folder_train, filename), dpi=100)
        else:
            fig.savefig(os.path.join(circles_folder_test, filename), dpi=100)

        plt.clf()

        ci_writer.writerow([filename, ci_x, ci_y, ci_radius, ci_area, ci_dfc, ci_dfc_f, ci_color, bg_color, variant])
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
        b = f"Generating Squares {i+1}/{size} "
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111, aspect='equal')
        bg_color = du.generate_nonmatching_color()
        exclude_colors = [bg_color]

        sq_area = distribution[i]
        sq_length = np.sqrt(sq_area)
        sq_x = np.random.uniform(0, img_width - sq_length)
        sq_y = np.random.uniform(0, img_height - sq_length)
        sq_angle = np.random.uniform(0, 360)
        sq_corners = du.get_square_corners(sq_x, sq_y, sq_length, sq_angle)

        while du.square_out_of_bounds(sq_corners, img_width, img_height):
            sq_x = np.random.uniform(0, img_width - sq_length)
            sq_y = np.random.uniform(0, img_height - sq_length)
            sq_angle = np.random.uniform(0, 360)
            sq_corners = du.get_square_corners(sq_x, sq_y, sq_length, sq_angle)

        sq_dfc = du.calculate_dfc_square(sq_x, sq_y, sq_length, sq_angle, img_width, img_height)
        sq_dfc_further = du.calculate_dfc_further_square(sq_x, sq_y, sq_length, sq_angle, img_width, img_height)
        sq_color = du.generate_nonmatching_color()

        square = patches.Rectangle((sq_x, sq_y), sq_length, sq_length, angle=sq_angle, color=sq_color, rotation_point="center")
        ax.add_patch(square)

        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        filename = f'squares_{counter}.png'
        if j == 0:
            fig.savefig(os.path.join(squares_folder_train, filename), dpi=100)
        else:
            fig.savefig(os.path.join(squares_folder_test, filename), dpi=100)

        plt.clf()

        sq_writer.writerow([filename, sq_x, sq_y, sq_length, sq_angle, sq_area, sq_dfc, sq_dfc_further, sq_corners, sq_color, bg_color, variant])
        counter += 1

# Nones
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    for i in range(size):
        b = f"Generating Nones {i+1}/{size} "
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111, aspect='equal')
        bg_color = du.generate_nonmatching_color()
        fig.set_facecolor(bg_color)

        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')

        filename = f'nones_{counter}.png'
        if j == 0:
            fig.savefig(os.path.join(nones_folder_train, filename), dpi=100)
        else:
            fig.savefig(os.path.join(nones_folder_test, filename), dpi=100)

        plt.clf()

        nones_writer.writerow([filename, bg_color, bg_color, variant])
        counter += 1

end = pc()
print(f"Time: {end-start} seconds")
