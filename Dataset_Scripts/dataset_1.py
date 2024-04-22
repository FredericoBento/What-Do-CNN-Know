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


# Dataset A
# Circles and Nones

circles_folder_train = 'Datasets/Dataset_A/train/circles'
circles_folder_test = 'Datasets/Dataset_A/test/circles'

nones_folder_train = 'Datasets/Dataset_A/train/nones'
nones_folder_test = 'Datasets/Dataset_A/test/nones'

data_folder = 'Datasets/Dataset_A/data'
seed = 42
np.random.seed(seed)

# Create data_folder if it does not exist
os.makedirs(data_folder, exist_ok=True)
os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)
os.makedirs(nones_folder_train, exist_ok=True)
os.makedirs(nones_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

# Circles (Not Cut)
start = pc()
circles_writer = csv.writer(open(os.path.join(data_folder, 'circles.csv'), 'w'))
circles_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Color', 'Bg_color', 'Distance From Center', 'Variant'])
fig = plt.figure(figsize=(img_width/100, img_height/100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
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
            x = np.random.uniform(0, img_width - radius)
            y = np.random.uniform(0, img_height - radius)
            # check if circle is outside of the image
            if du.circle_out_of_bounds(x, y, radius, img_width, img_height):
                tries += 1
                continue
            all_ok = True

        bg_color = du.generate_nonmatching_color()
        color = du.generate_nonmatching_color(bg_color)
        area = np.pi * radius ** 2
        dfc = du.calculate_dfc_circle(x, y, radius, img_width, img_height)
        dfc = round(dfc, 2)
        area = round(area, 2)
        circles_writer.writerow([f'circle_{counter}.png', x, y, radius, area, color, bg_color, dfc, variant])
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
        path = os.path.join(folder, f'circle_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1

# Nones
print("\n")
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
