import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patches
import csv
import os
import dataset_utils as du
from time import perf_counter as pc
matplotlib.use('QtAgg')


# Dataset B
# Squares and Nones

squares_folder_train = 'Datasets/Dataset_B/train/squares'
squares_folder_test = 'Datasets/Dataset_B/test/squares'

nones_folder_train = 'Datasets/Dataset_B/train/nones'
nones_folder_test = 'Datasets/Dataset_B/test/nones'

data_folder = 'Datasets/Dataset_B/data'
seed = 111
np.random.seed(seed)

train_size = int(11_000 / 2)
test_size = int(5_000 / 2)

img_width = 500
img_height = 500

min_square_length = 10
max_square_length = img_width / 2

min_square_area = min_square_length ** 2
max_square_area = max_square_length ** 2

# Create data_folder if it does not exist
os.makedirs(data_folder, exist_ok=True)
os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)
os.makedirs(nones_folder_train, exist_ok=True)
os.makedirs(nones_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

# Squares(Not Cut)
start = pc()
squares_writer = csv.writer(open(os.path.join(data_folder, 'squares.csv'), 'w'))
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Area', 'Angle', 'Color', 'Bg_color', 'Distance From Center', 'Variant'])
fig = plt.figure(figsize=(img_width/100, img_height/100))
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
            # check if square is outside of the image
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
        # dfc = (x2 - x1)^2 + (y2 - y1)^2
        dfc = np.sqrt((center_x - img_width/2) ** 2 + (center_y - img_height/2) ** 2)
        squares_writer.writerow([f'square_{counter}.png', x, y, length, area, angle, color, bg_color, dfc, variant])
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

# Nones
print("\r", flush=True)
counter = 1
for j in range(2):
    if j == 0:
        size = train_size
    else:
        size = test_size
    for i in range(size):
        b = f"Generating Nones {i+1}/{size}"
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111)
        fig.set_facecolor(du.generate_nonmatching_color())
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        plt.clf()
        if j == 0:
            folder = nones_folder_train
        else:
            folder = nones_folder_test
        plt.savefig(os.path.join(folder, f'none_{counter}.png'))
        counter += 1

end = pc()
print(f"Finished generating images ({round(end - start, 4)}s)")
