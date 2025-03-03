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


circle_folder_train = 'Datasets/Dataset_R2/train/circles'
circle_folder_test = 'Datasets/Dataset_R2/test/circles'

data_folder = 'Datasets/Dataset_R2/data'
seed = 122
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(circle_folder_train, exist_ok=True)
os.makedirs(circle_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

start = pc()
ci_big_writer = csv.writer(open(os.path.join(data_folder, 'circles_big.csv'), 'w'))
ci_big_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Distance From Center', 'Distance From Center Further', 'Proportion', 'Distance', 'Color', 'Bg_color', 'Variant'])

ci_small_writer = csv.writer(open(os.path.join(data_folder, 'circles_small.csv'), 'w'))
ci_small_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Distance From Center', 'Distance From Center Further', 'Proportion', 'Distance', 'Color', 'Bg_color', 'Variant'])

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

    distribution = np.random.uniform(min_circle_area, max_circle_area, int(size / 2))
    for i in range(size):
        b = f"Generating Circles {i+1}/{size} "
        print(b, end='\r', flush=True)

        ax = fig.add_subplot(111, aspect='equal')
        exclude_colors = []

        # Generate Big Circle
        ci_big_area = np.random.choice(distribution)
        ci_big_radius = np.sqrt(ci_big_area / np.pi)
        ci_big_x = np.random.uniform(0 + ci_big_radius, img_width - ci_big_radius)
        ci_big_y = np.random.uniform(0 + ci_big_radius, img_height - ci_big_radius)
        ci_big_dfc = du.calculate_dfc_circle(ci_big_x, ci_big_y, ci_big_radius, img_width, img_height)
        ci_big_dfc_f = du.calculate_dfc_further_circle(ci_big_x, ci_big_y, ci_big_radius, img_width, img_height)
        ci_big_color = du.generate_nonmatching_color()
        exclude_colors.append(ci_big_color)

        # Generate Small Circle
        ci_small_area = np.random.choice(distribution)
        while ci_big_area <= ci_small_area:
            ci_small_area = np.random.uniform(min_circle_area, ci_big_area)

        if ci_big_area < ci_small_area:
            print('Error: Big Circle Area < Small Circle Area')
            print(f'Big Circle Area: {ci_big_area}')
            print(f'Small Circle Area: {ci_small_area}')

        # Repeat while there is intersection
        lock_limit = 100
        lock_times = 0
        intersect = True
        while intersect is True:
            if lock_times > lock_limit:
                # change size and try again
                ci_small_area = np.random.choice(distribution)
                lock_times = 0

            ci_small_radius = np.sqrt(ci_small_area / np.pi)
            ci_small_x = np.random.uniform(0 + ci_small_radius, img_width - ci_small_radius)
            ci_small_y = np.random.uniform(0 + ci_small_radius, img_height - ci_small_radius)

            intersect = du.circle_intersect_circle(ci_big_x, ci_big_y, ci_big_radius, ci_small_x, ci_small_y, ci_small_radius)
            lock_times += 1

        ci_small_dfc = du.calculate_dfc_circle(ci_small_x, ci_small_y, ci_small_radius, img_width, img_height)
        ci_small_dfc_f = du.calculate_dfc_further_circle(ci_small_x, ci_small_y, ci_small_radius, img_width, img_height)
        ci_small_color = du.generate_nonmatching_color(exclude_colors)
        exclude_colors.append(ci_small_color)

        # Proportion
        big_proportion = ci_big_area / ci_small_area
        big_proportion = round(big_proportion, 3)

        small_proportion = ci_small_area / ci_big_area
        small_proportion = round(small_proportion, 3)

        distance_between_centers = np.sqrt((ci_big_x - ci_small_x)**2 + (ci_big_y - ci_small_y)**2)
        distance_between_centers = round(distance_between_centers, 3)

        # Draw circles
        ax.add_patch(patches.Circle((ci_big_x, ci_big_y), ci_big_radius, color=ci_big_color))
        ax.add_patch(patches.Circle((ci_small_x, ci_small_y), ci_small_radius, color=ci_small_color))

        # Finish plot and save
        bg_color = du.generate_nonmatching_color(exclude_colors)
        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        filename = f'circles_{counter}.png'
        if j == 0:
            fig.savefig(os.path.join(circle_folder_train, filename), dpi=100)
        else:
            fig.savefig(os.path.join(circle_folder_test, filename), dpi=100)

        plt.clf()
        # Write CSV
        ci_big_writer.writerow([filename, ci_big_x, ci_big_y, ci_big_radius, ci_big_area, ci_big_dfc, ci_big_dfc_f, big_proportion, distance_between_centers, ci_big_color, bg_color, variant])
        ci_small_writer.writerow([filename, ci_small_x, ci_small_y, ci_small_radius, ci_small_area, ci_small_dfc, ci_small_dfc_f, small_proportion, distance_between_centers, ci_small_color, bg_color, variant])
        counter += 1

end = pc()
print(f"Time: {round(end - start, 3)}")
