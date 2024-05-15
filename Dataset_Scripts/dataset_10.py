import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
import csv
import os
from time import perf_counter as pc
import dataset_utils as du
import multiprocessing
from variables import *

matplotlib.use('TkAgg')


# Dataset 9 Circles, Squares, Triangles

circles_folder_train = 'Datasets/Dataset_10/train/circles'
circles_folder_test = 'Datasets/Dataset_10/test/circles'

squares_folder_train = 'Datasets/Dataset_10/train/squares'
squares_folder_test = 'Datasets/Dataset_10/test/squares'

triangles_folder_train = 'Datasets/Dataset_10/train/triangles'
triangles_folder_test = 'Datasets/Dataset_10/test/triangles'

data_folder = 'Datasets/Dataset_10/data'
seed = 181
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)

os.makedirs(circles_folder_train, exist_ok=True)
os.makedirs(circles_folder_test, exist_ok=True)

os.makedirs(squares_folder_train, exist_ok=True)
os.makedirs(squares_folder_test, exist_ok=True)

os.makedirs(triangles_folder_train, exist_ok=True)
os.makedirs(triangles_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))
file.close()

start = pc()
ci_file = open(os.path.join(data_folder, 'circles.csv'), 'w')
ci_writer = csv.writer(ci_file)
ci_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Distance From Center', 'Distance From Center Further', 'Color', 'Bg_color', 'Variant'])

sq_file = open(os.path.join(data_folder, 'squares.csv'), 'w')
sq_writer = csv.writer(sq_file)
sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Distance From Center', 'Distance From Center Further', 'Corners', 'Color', 'Bg_color', 'Variant'])

tr_file = open(os.path.join(data_folder, 'triangles.csv'), 'w')
tr_writer = csv.writer(tr_file)
tr_writer.writerow(['Filename', 'X', 'Y', 'Side 1', 'Side 2', 'Base', 'Area', 'Distance From Center', 'Distance From Center Further', 'Corners', 'Color', 'Bg_color', 'Variant'])

lock = multiprocessing.Lock()

def gen_circles():
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
            ci_area = round(ci_area, 3)
            ci_radius = np.sqrt(ci_area / np.pi)
            ci_radius = round(ci_radius, 3)
            ci_x = np.random.uniform(0 + ci_radius, img_width - ci_radius)
            ci_y = np.random.uniform(0 + ci_radius, img_height - ci_radius)

            while du.circle_out_of_bounds(ci_x, ci_y, ci_radius, img_width, img_height):
                ci_x = np.random.uniform(0 + ci_radius, img_width - ci_radius)
                ci_y = np.random.uniform(0 + ci_radius, img_height - ci_radius)

            ci_dfc = du.calculate_dfc_circle(ci_x, ci_y, ci_radius, img_width, img_height)
            ci_dfc_f = du.calculate_dfc_further_circle(ci_x, ci_y, ci_radius, img_width, img_height)
            ci_color = du.generate_nonmatching_color()
            exclude_colors.append(ci_color)

            ci_x = round(ci_x, 3)
            ci_y = round(ci_y, 3)
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

            lock.acquire()
            ci_writer.writerow([filename, ci_x, ci_y, ci_radius, ci_area, ci_dfc, ci_dfc_f, ci_color, bg_color, variant])
            counter += 1
            lock.release()
    ci_file.flush()
    ci_file.close()


def gen_squares():
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

            lock.acquire()
            sq_writer.writerow([filename, sq_x, sq_y, sq_length, sq_angle, sq_area, sq_dfc, sq_dfc_further, sq_corners, sq_color, bg_color, variant])
            counter += 1
            lock.release()
    sq_file.flush()
    sq_file.close()

# Triangles


def gen_triangles():
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

        distribution = np.random.uniform(min_triangle_area, max_triangle_area, size)

        for i in range(size):
            b = f"Generating Triangles {i+1}/{size} "
            print(b, end='\r', flush=True)

            area = distribution[i]

            ax = fig.add_subplot(111, aspect='equal')
            bg_color = du.generate_nonmatching_color()
            exclude_colors = [bg_color]

            discount = area * 0.1
            tr_area = -1
            tries = 1000
            while tr_area < area - discount or tr_area > area + discount:
                tr_x = np.random.uniform(0, img_width)
                tr_y = np.random.uniform(0, img_height)
                tr_x = round(tr_x, 2)
                tr_y = round(tr_y, 2)
                tr_s1, tr_s2, tr_base = du.random_triangle()
                tr_angle = np.random.uniform(0, 360)
                tr_corners = du.get_triangle_corners(tr_x, tr_y, tr_s1, tr_s2, tr_base, tr_angle)

                while tr_corners is None:
                    tr_s1, tr_s2, tr_base = du.random_triangle()
                    tr_corners = du.get_triangle_corners(tr_x, tr_y, tr_s1, tr_s2, tr_base, tr_angle)

                while du.triangle_out_of_bounds(tr_corners, img_width, img_height):
                    tr_x = np.random.uniform(0, img_width)
                    tr_y = np.random.uniform(0, img_height)
                    tr_x = round(tr_x, 2)
                    tr_y = round(tr_y, 2)
                    angle = np.random.uniform(0, 360)
                    tr_corners = du.get_triangle_corners(tr_x, tr_y, tr_s1, tr_s2, tr_base, tr_angle)
                    while tr_corners is None:
                        tr_s1, tr_s2, tr_base = du.random_triangle()
                        tr_corners = du.get_triangle_corners(tr_x, tr_y, tr_s1, tr_s2, tr_base, tr_angle)

                tr_area = du.get_triangle_area(tr_corners)
                tries -= 1
                if tries == 0:
                    area = np.random.uniform(min_triangle_area, max_triangle_area)
                    tries = 1000

            tr_dfc = du.calculate_dfc_triangle(tr_corners, img_width, img_height)
            tr_dfc_further = du.calculate_dfc_further_triangle(tr_corners, img_width, img_height)

            tr_color = du.generate_nonmatching_color()

            triangle = patches.Polygon(tr_corners, color=tr_color)
            ax.add_patch(triangle)

            fig.set_facecolor(bg_color)
            ax.set_xlim(0, img_width)
            ax.set_ylim(0, img_height)
            ax.axis('off')
            filename = f'triangles_{counter}.png'
            if j == 0:
                fig.savefig(os.path.join(triangles_folder_train, filename), dpi=100)
            else:
                fig.savefig(os.path.join(triangles_folder_test, filename), dpi=100)

            plt.clf()

            lock.acquire()
            tr_writer.writerow([filename, tr_x, tr_y, tr_s1, tr_s2, tr_base, tr_area, tr_dfc, tr_dfc_further, tr_corners, tr_color, bg_color, variant])
            counter += 1
            lock.release()
    tr_file.flush()
    tr_file.close()


prc1 = multiprocessing.Process(target=gen_circles)
prc2 = multiprocessing.Process(target=gen_squares)
prc3 = multiprocessing.Process(target=gen_triangles)

prc1.start()
prc2.start()
prc3.start()

prc1.join()
prc2.join()
prc3.join()


end = pc()
print(f"Time: {end-start} seconds")
