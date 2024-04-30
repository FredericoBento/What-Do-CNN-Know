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


# Dataset 6.1
# Mutiple Squares Cut and Mutiple Circles Cut

squares_folder_train = 'Datasets/Dataset_6_1/train/squares_cut'
squares_folder_test = 'Datasets/Dataset_6_1/test/squares_cut'

circles_folder_train = 'Datasets/Dataset_6_1/train/circles_cut'
circles_folder_test = 'Datasets/Dataset_6_1/test/circles_cut'

data_folder = 'Datasets/Dataset_6_1/data'
seed = 565
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)
os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

# Squares Cut
start = pc()
squares_writer = csv.writer(open(os.path.join(data_folder, 'squares_cut.csv'), 'w'))
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Corners', 'Cut', 'Variant'])

circles_writer = csv.writer(open(os.path.join(data_folder, 'circles_cut.csv'), 'w'))
circles_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Cut', 'Variant'])

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

    distribution = np.random.uniform(min_square_area, max_square_area, size)
    count_distribution = np.random.randint(1, 6, size)
    for i in range(size):
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        ax = fig.add_subplot(111, aspect='auto')
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
                    # length = np.sqrt(distribution[i])
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
                visible_area = du.calculate_visible_area_square(x, y, length, angle, img_width, img_height)
                dfc = du.calculate_dfc_square(x, y, length, angle, img_width, img_height)
                dfc = round(dfc, 2)
                area = round(area, 2)
                visible_area = round(visible_area, 2)
                squares_writer.writerow([f'square_cut_{counter}.png', x, y, length, angle, area, visible_area, color, bg_color, dfc, corners, "True", variant])
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
    count_distribution = np.random.randint(1, 6, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='equal')
        b = f"Generating Circles {i+1}/{size}"
        print(b, end='\r', flush=True)
        circles = []
        bg_color = du.generate_nonmatching_color()
        excluded_colors = [bg_color]
        k = 0
        while k < int(count_distribution[i]):
            all_ok = False
            tries = 0
            max_tries = 10
            while all_ok is False:
                if tries >= max_tries:
                    radius = np.random.uniform(min_circle_area, max_circle_area)
                    radius = np.sqrt(radius/np.pi)
                    tries = 0
                else:
                    radius = np.sqrt(np.random.choice(distribution)/np.pi)
                x = np.random.uniform(0-radius+outside_min, img_width + radius - outside_min)
                y = np.random.uniform(0-radius+outside_min, img_height + radius - outside_min)
                if du.circle_is_cut(x, y, radius, img_width, img_height) is False:
                    tries += 1
                    continue

                overlap = False
                for c in circles:
                    if du.circle_overlap(x, y, radius, c[0], c[1], c[2]) is True:
                        overlap = True
                        break

                if overlap is True:
                    tries += 1
                    continue
                else:
                    all_ok = True

                circles.append([x, y, radius])
                color = du.generate_nonmatching_color(excluded_colors)
                excluded_colors.append(color)
                area = np.pi * radius ** 2
                visible_area = du.calculate_visible_area_circle(x, y, radius, img_width, img_height)
                dfc = du.calculate_dfc_circle(x, y, radius, img_width, img_height)
                dfc = round(dfc, 2)
                area = round(area, 2)
                visible_area = round(visible_area, 2)
                circles_writer.writerow([f'circle_cut_{counter}.png', x, y, radius, area, visible_area, color, bg_color, dfc, "True", variant])
                circle = patches.Circle((x, y), radius, color=color)
                ax.add_patch(circle)
            k += 1
        fig.set_facecolor(bg_color)
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
