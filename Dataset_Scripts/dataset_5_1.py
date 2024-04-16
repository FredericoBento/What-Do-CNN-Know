import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patches
import csv
import os
import dataset_utils as du
from time import perf_counter as pc
matplotlib.use('QtAgg')


# Dataset 5_1
# Mutiple Squares Cut and Mutiple Squares

squares_folder_train = 'Datasets/Dataset_5_1/train/squares'
squares_folder_test = 'Datasets/Dataset_5_1/test/squares'

squares_cut_folder_train = 'Datasets/Dataset_5_1/train/squares_cut'
squares_cut_folder_test = 'Datasets/Dataset_5_1/test/squares_cut'

data_folder = 'Datasets/Dataset_5_1/data'
seed = 328
np.random.seed(seed)

train_size = int(100 / 2)
test_size = int(50 / 2)

img_width = 500
img_height = 500

min_square_length = 10
max_square_length = img_width / 2

min_square_area = min_square_length ** 2
max_square_area = max_square_length ** 2

min_circle_radius = 10
max_circle_radius = img_width / 4

min_circle_area = np.pi * min_circle_radius ** 2
max_circle_area = np.pi * max_circle_radius ** 2

outside_min = 5

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
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Area', 'Angle', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

squares_cut_writer = csv.writer(open(os.path.join(data_folder, 'squares_cut.csv'), 'w'))
squares_cut_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Area', 'Visible Area', 'Angle', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

fig = plt.figure(figsize=(img_width/100, img_height/100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Mutiple Squares Cut
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_area, max_square_area, size)
    count_distribution = np.random.randint(1, 6, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='equal')
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        square_corners = []
        excluded_colors = [bg_color]
        # for k in range(int(count_distribution[i])):
        k = 0
        while k < int(count_distribution[i]):
            all_ok = False
            tries = 0
            max_tries = 10
            while all_ok is False:
                if tries >= max_tries:
                    length = np.random.uniform(min_square_area, max_square_area)
                    length = np.sqrt(length)
                    tries = 0
                else:
                    length = np.sqrt(np.random.choice(distribution))

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

                overlap = False
                for c in square_corners:
                    if du.square_overlap(corners, c) is True:
                        overlap = True
                        break

                if overlap is True:
                    tries += 1
                    continue
                else:
                    all_ok = True

                square_corners.append(corners)
                color = du.generate_nonmatching_color(excluded_colors)
                excluded_colors.append(color)
                area = length ** 2
                visible_area = du.calculate_visible_area([x], [y], [length], img_width, img_height)
                dfc = np.sqrt((center_x - img_width/2) ** 2 + (center_y - img_height/2) ** 2)
                squares_cut_writer.writerow([f'square_cut_{counter}.png', x, y, length, area, visible_area, angle, color, bg_color, dfc, corners, "True", variant])
                square.set_color(color)
                ax.add_patch(square)
            k += 1
        fig.set_facecolor(bg_color)
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

# Mutiple Squares
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_area, max_square_area, size)
    count_distribution = np.random.randint(1, 6, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='auto')
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        square_corners = []
        excluded_colors = [bg_color]
        k = 0
        while k < int(count_distribution[i]):
            all_ok = False
            tries = 0
            max_tries = 10
            while all_ok is False:
                if tries >= max_tries:
                    length = np.random.uniform(min_square_area, max_square_area)
                    length = np.sqrt(length)
                    tries = 0
                else:
                    length = np.sqrt(np.random.choice(distribution))

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

                overlap = False
                for c in square_corners:
                    if du.square_overlap(corners, c) is True:
                        overlap = True
                        break

                if overlap is True:
                    tries += 1
                    continue
                else:
                    all_ok = True

                square_corners.append(corners)
                color = du.generate_nonmatching_color(excluded_colors)
                excluded_colors.append(color)
                area = length ** 2
                dfc = np.sqrt((center_x - img_width/2) ** 2 + (center_y - img_height/2) ** 2)
                squares_writer.writerow([f'square_{counter}.png', x, y, length, area, angle, color, bg_color, dfc, variant])
                square.set_color(color)
                ax.add_patch(square)
            k += 1
        fig.set_facecolor(bg_color)
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
        # square_corners.clear()
