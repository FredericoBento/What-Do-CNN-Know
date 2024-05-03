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


# Dataset 2 Squares with different sizes, per image

square_folder_train = 'Datasets/Dataset_8_1/train/squares'
square_folder_test = 'Datasets/Dataset_8_1/test/squares'

data_folder = 'Datasets/Dataset_8_1/data'
seed = 123
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(square_folder_train, exist_ok=True)
os.makedirs(square_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()
sq_big_writer = csv.writer(open(os.path.join(data_folder, 'squares_big.csv'), 'w'))
sq_big_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Distance From Center', 'Distance From Center Further', 'Proportion', 'Corners', 'Color', 'Bg_color', 'Variant'])

sq_small_writer = csv.writer(open(os.path.join(data_folder, 'squares_small.csv'), 'w'))
sq_small_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Distance From Center', 'Distance From Center Further', 'Proportion', 'Corners', 'Color', 'Bg_color', 'Variant'])

fig = plt.figure(figsize=(img_width/100, img_height/100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_area, max_square_area, int(size / 2))
    for i in range(size):
        b = f"Generating squares {i+1}/{size} "
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111, aspect='equal')
        exclude_colors = []

        # Generate Big Square
        sq_big_area = np.random.choice(distribution)
        sq_big_area = round(sq_big_area, 2)
        sq_big_length = np.sqrt(sq_big_area)

        out_of_bounds = True
        while out_of_bounds:
            sq_big_x = np.random.uniform(0, img_width - sq_big_length)
            sq_big_y = np.random.uniform(0, img_height - sq_big_length)
            sq_big_angle = np.random.uniform(0, 360)
            sq_big_corners = du.get_square_corners(sq_big_x, sq_big_y, sq_big_length, sq_big_angle)
            if du.square_out_of_bounds(sq_big_corners, img_width, img_height) is False:
                out_of_bounds = False

        sq_big_dfc = du.calculate_dfc_square(sq_big_x, sq_big_y, sq_big_length, sq_big_angle, img_width, img_height)
        sq_big_dfc_f = du.calculate_dfc_further_square(sq_big_x, sq_big_y, sq_big_length, sq_big_angle, img_width, img_height)
        sq_big_color = du.generate_nonmatching_color()
        exclude_colors.append(sq_big_color)

        # Generate Small Square
        sq_small_area = np.random.choice(distribution)
        lock_limit = 100
        lock_times = 0
        while sq_big_area <= sq_small_area:
            if lock_times > lock_limit:
                sq_small_area = np.random.uniform(min_square_area, sq_big_area)
                lock_times = 0
            else:
                sq_small_area = np.random.choice(distribution)
                lock_times += 1

        # Repeat while there is intersection
        lock_limit = 100
        lock_times = 0
        intersect = True
        while intersect is True:
            if lock_times > lock_limit:
                # change size and try again
                sq_small_area = np.random.choice(distribution)

            sq_small_length = np.sqrt(sq_small_area)
            sq_small_x = np.random.uniform(0, sq_small_length)
            sq_small_y = np.random.uniform(0, img_height - sq_small_length)
            sq_small_angle = np.random.uniform(0, 360)
            sq_small_corners = du.get_square_corners(sq_small_x, sq_small_y, sq_small_length, sq_small_angle)

            if du.square_out_of_bounds(sq_small_corners, img_width, img_height) is False:
                intersect = du.square_intersect_square(sq_big_corners, sq_small_corners)

            lock_times += 1

        sq_small_dfc = du.calculate_dfc_square(sq_small_x, sq_small_y, sq_small_length, sq_small_angle, img_width, img_height)
        sq_small_dfc_f = du.calculate_dfc_further_square(sq_small_x, sq_small_y, sq_small_length, sq_small_angle, img_width, img_height)
        sq_small_color = du.generate_nonmatching_color(exclude_colors)
        exclude_colors.append(sq_small_color)

        # Proportion
        big_proportion = sq_big_area / sq_small_area
        big_proportion = round(big_proportion, 2)

        small_proportion = sq_small_area / sq_big_area
        small_proportion = round(small_proportion, 2)

        # Draw squares
        ax.add_patch(patches.Rectangle((sq_big_x, sq_big_y), sq_big_length, sq_big_length, angle=sq_big_angle, color=sq_big_color, rotation_point="center"))
        ax.add_patch(patches.Rectangle((sq_small_x, sq_small_y), sq_small_length, sq_small_length, angle=sq_small_angle, color=sq_small_color, rotation_point="center"))

        # Finish plot and save
        bg_color = du.generate_nonmatching_color(exclude_colors)
        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        filename = f'squares_{counter}.png'
        if j == 0:
            fig.savefig(os.path.join(square_folder_train, filename), dpi=100)
        else:
            fig.savefig(os.path.join(square_folder_test, filename), dpi=100)

        plt.clf()

        # Write CSV
        sq_big_writer.writerow([filename, sq_big_x, sq_big_y, sq_big_length, sq_big_area, sq_big_dfc, sq_big_dfc_f, big_proportion, sq_big_corners, sq_big_color, bg_color, variant])
        sq_small_writer.writerow([filename, sq_small_x, sq_small_y, sq_small_length, sq_small_area, sq_small_dfc, sq_small_dfc_f, small_proportion, sq_small_corners, sq_small_color, bg_color, variant])
        counter += 1

end = pc()
print(f"Time: {round(end - start, 3)}")
