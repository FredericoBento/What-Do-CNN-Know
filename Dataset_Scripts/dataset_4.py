import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patches
import csv
import os
import dataset_utils as du
from time import perf_counter as pc
matplotlib.use('QtAgg')


# Dataset 4
# Circles Cut and Circles

circles_folder_train = 'Datasets/Dataset_4/train/circles'
circles_folder_test = 'Datasets/Dataset_4/test/circles'

circles_cut_folder_train = 'Datasets/Dataset_4/train/circles_cut'
circles_cut_folder_test = 'Datasets/Dataset_4/test/circles_cut'

data_folder = 'Datasets/Dataset_4/data'
seed = 674
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
os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)
os.makedirs(circles_cut_folder_test, exist_ok=True)
os.makedirs(circles_cut_folder_train, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()

circles_writer = csv.writer(open(os.path.join(data_folder, 'circles.csv'), 'w'))
circles_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Color', 'Bg_color', 'Distance From Center', 'Cut', 'Variant'])

circles_cut_writer = csv.writer(open(os.path.join(data_folder, 'circles_cut.csv'), 'w'))
circles_cut_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Color', 'Bg_color', 'Distance From Center', 'Cut', 'Variant'])

fig = plt.figure(figsize=(img_width/100, img_height/100))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Circles Cut
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
        dfc = np.sqrt((x - img_width/2) ** 2 + (y - img_height/2) ** 2)
        circles_cut_writer.writerow([f'circle_cut_{counter}.png', x, y, radius, area, visible_area, color, bg_color, dfc, "True", variant])
        fig.set_facecolor(bg_color)
        circle = patches.Circle((x, y), radius, color=color)
        ax.add_patch(circle)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = circles_cut_folder_train
        else:
            folder = circles_cut_folder_test
        path = os.path.join(folder, f'circle_cut_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1

# Circles
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
        dfc = np.sqrt((x - img_width/2) ** 2 + (y - img_height/2) ** 2)
        circles_writer.writerow([f'circle_{counter}.png', x, y, radius, area, color, bg_color, dfc, "False", variant])
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

end = pc()
print(f"Finished generating images ({round(end - start, 4)}s)")
