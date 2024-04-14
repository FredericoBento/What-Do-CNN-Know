import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import patches
import csv
import os
import dataset_utils as du
from time import perf_counter as pc
matplotlib.use('QtAgg')


# Dataset 3_1
# Mutiplos Circulos / Mutiplos Quadrados

squares_folder_train = 'Datasets/Dataset_3_1/train/squares'
squares_folder_test = 'Datasets/Dataset_3_1/test/squares'

circles_folder_train = 'Datasets/Dataset_3_1/train/circles'
circles_folder_test = 'Datasets/Dataset_3_1/test/circles'

data_folder = 'Datasets/Dataset_3_1/data'
seed = 120
np.random.seed(seed)

train_size = int(3000 / 2)
test_size = int(1000 / 2)

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

os.makedirs(data_folder, exist_ok=True)
os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)
os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))

# Squares(Not Cut)
start = pc()
squares_writer = csv.writer(open(os.path.join(data_folder, 'squares.csv'), 'w'))
squares_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Area', 'Angle', 'Color', 'Bg_color', 'Distance From Center', 'Variant'])

circles_writer = csv.writer(open(os.path.join(data_folder, 'circles.csv'), 'w'))
circles_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Color', 'Bg_color', 'Distance From Center', 'Variant'])

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
    count_distribution = np.random.randint(1, 5, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='auto')
        b = f"Generating Square {i+1}/{size}"
        print(b, end='\r', flush=True)
        square_corners = []
        for k in range(count_distribution[i]+1):
            all_ok = False
            tries = 0
            max_tries = 10
            bg_color = du.generate_nonmatching_color()
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
                # check if square is outside of the image
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
                color = du.generate_nonmatching_color(bg_color)
                area = length ** 2
                # dfc = (x2 - x1)^2 + (y2 - y1)^2
                dfc = np.sqrt((center_x - img_width/2) ** 2 + (center_y - img_height/2) ** 2)
                squares_writer.writerow([f'square_{counter}.png', x, y, length, area, angle, color, bg_color, dfc, variant])
                square.set_color(color)
                ax.add_patch(square)

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
        square_corners.clear()

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
    count_distribution = np.random.randint(1, 5, size)
    for i in range(size):
        ax = fig.add_subplot(111, aspect='equal')
        b = f"Generating Circles {i+1}/{size}"
        print(b, end='\r', flush=True)
        circles = []
        for k in range(count_distribution[i]+1):
            all_ok = False
            tries = 0
            max_tries = 10
            bg_color = du.generate_nonmatching_color()
            while all_ok is False:
                if tries >= max_tries:
                    radius = np.random.uniform(min_circle_area, max_circle_area)
                    radius = np.sqrt(radius/np.pi)
                    tries = 0
                else:
                    # radius = np.sqrt(distribution[i]/np.pi)
                    radius = np.sqrt(np.random.choice(distribution)/np.pi)
                x = np.random.uniform(0, img_width - radius)
                y = np.random.uniform(0, img_height - radius)
                # check if circle is outside of the image
                if du.circle_out_of_bounds(x, y, radius, img_width, img_height):
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
                color = du.generate_nonmatching_color(bg_color)
                area = np.pi * radius ** 2
                # dfc = (x2 - x1)^2 + (y2 - y1)^2
                dfc = np.sqrt((x - img_width/2) ** 2 + (y - img_height/2) ** 2)
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

end = pc()
print(f"Finished generating images ({round(end - start, 4)}s)")
