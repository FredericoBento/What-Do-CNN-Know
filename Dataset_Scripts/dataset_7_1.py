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


# Dataset 7_1
# 7 but with overlaping

sar_folder_train = 'Datasets/Dataset_7_1/train/squares_at_right'
sar_folder_test = 'Datasets/Dataset_7_1/test/squares_at_right'

car_folder_train = 'Datasets/Dataset_7_1/train/circles_at_right'
car_folder_test = 'Datasets/Dataset_7_1/test/circles_at_right'

data_folder = 'Datasets/Dataset_7_1/data'
seed = 323
np.random.seed(seed)

os.makedirs(data_folder, exist_ok=True)
os.makedirs(sar_folder_train, exist_ok=True)
os.makedirs(sar_folder_test, exist_ok=True)
os.makedirs(car_folder_train, exist_ok=True)
os.makedirs(car_folder_test, exist_ok=True)

# Save seed
file = open(os.path.join(data_folder, 'seed.txt'), 'w')
file.write(str(seed))


start = pc()
sar_sq_writer = csv.writer(open(os.path.join(data_folder, 'sar_sq.csv'), 'w'))
sar_ci_writer = csv.writer(open(os.path.join(data_folder, 'sar_ci.csv'), 'w'))
sar_ci_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Distance From Center',
                        'Distance From Center Further', 'Color', 'Bg_color', 'Position', 'Cut', 'Variant'])

sar_sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Distance From Center'
                        , 'Distance From Center Further',
                        'Corners', 'Color', 'Bg_color', 'Position', 'Cut', 'Variant'])

car_sq_writer = csv.writer(open(os.path.join(data_folder, 'car_sq.csv'), 'w'))
car_ci_writer = csv.writer(open(os.path.join(data_folder, 'car_ci.csv'), 'w'))
car_ci_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Distance From Center',
                        'Distance From Center Further', 'Color', 'Bg_color', 'Position', 'Cut', 'Variant'])

car_sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Distance From Center'
                        , 'Distance From Center Further',
                        'Corners', 'Color', 'Bg_color', 'Position', 'Cut', 'Variant'])

max_square_area = 150 ** 2
# car (circle at right)
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

    distribution = np.random.uniform(min_square_length, 150, size)
    do_2_ci = False
    for i in range(size):
        if i >= size / 2:
            do_2_ci = True

        b = f"Generating car {i+1}/{size} "
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        ax = fig.add_subplot(111, aspect='auto')
        excluded_colors = [bg_color]
        dist_value = distribution[i]
        radius = dist_value / 2
        sq_intersected = False
        ci_intersected = False
        if do_2_ci is False:
            # add square at left
            length = dist_value
            all_ok = False
            while all_ok is False:
                sq_x = np.random.uniform(0, img_width - length)
                sq_y = np.random.uniform(0, img_height - length)
                angle = np.random.uniform(0, 360)
                sq_center_x = sq_x + length / 2
                sq_center_y = sq_y + length / 2

                square = patches.Rectangle((sq_x, sq_y), length, length, angle=angle, rotation_point=(sq_center_x, sq_center_y))
                corners = square.get_corners()

                if du.square_out_of_bounds(corners, img_width, img_height) is True:
                    continue

                if du.square_is_at_right(corners, img_width, img_height):
                    continue

                all_ok = True

            sq_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(sq_color)
            square.set_color(sq_color)
            sq_dfc = du.calculate_dfc_square(sq_x, sq_y, length, angle, img_width, img_height)
            sq_dfc_f = du.calculate_dfc_further_square(sq_x, sq_y, length, angle, img_width, img_height)
            sq_area = round(length ** 2, 2)
            sq_visible_area = sq_area

        else:
            # add circle at left
            all_ok = False
            while all_ok is False:
                ci_left_x = np.random.uniform(0 + radius, img_width - radius)
                ci_left_y = np.random.uniform(0 + radius, img_height - radius)

                if du.circle_out_of_bounds(ci_left_x, ci_left_y, radius, img_width, img_height):
                    continue

                if du.circle_is_at_right(ci_left_x, radius, img_width):
                    continue

                all_ok = True

            ci_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(ci_left_color)
            ci_left_dfc = du.calculate_dfc_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_dfc_f = du.calculate_dfc_further_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_area = round(np.pi * radius ** 2, 2)
            ci_left_visible_area = ci_left_area
            cal = patches.Circle((ci_left_x, ci_left_y), radius, color=ci_left_color)

        all_ok = False
        while all_ok is False:
            # add the circle at right
            ci_x = np.random.uniform(0 + radius, img_width - radius)
            ci_y = np.random.uniform(0 + radius, img_height - radius)

            if du.circle_out_of_bounds(ci_x, ci_y, radius, img_width, img_height):
                continue

            if du.circle_is_at_right(ci_x, radius, img_width) is False:
                continue

            # check if square is more to the right
            sqar = False
            if do_2_ci is False:
                for corner in corners:
                    if corner[0] >= (ci_x + radius):
                        sqar = True
                        break

            if sqar is True:
                continue

            # check overlaps
            if do_2_ci is False:
                if du.circle_intersect_square(ci_x, ci_y, radius, corners) is True:
                    sq_intersected = True
            else:
                if du.circle_intersect_circle(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius) is True:
                    ci_intersected = True

            all_ok = True

        ci_color = du.generate_nonmatching_color(excluded_colors)
        ci_dfc = du.calculate_dfc_circle(ci_x, ci_y, radius, img_width, img_height)
        ci_dfc_f = du.calculate_dfc_further_circle(ci_x, ci_y, radius, img_width, img_height)
        ci_area = round(np.pi * radius ** 2, 2)
        ci_visible_area = ci_area
        car = patches.Circle((ci_x, ci_y), radius, color=ci_color)

        # handle intersected visible areas
        if sq_intersected is True or ci_intersected is True:
            # decide if circle is under or above
            put_circle_under = np.random.choice([True, False])
            if put_circle_under is True:
                print(counter)
                if sq_intersected is True:
                    intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_x, ci_y, radius)
                    square.set_color(sq_color)
                    square.zorder = 2
                    ax.add_patch(square)
                else:
                    intersected_area = du.calculate_intersect_area_ci_ci(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius)
                    cal.zorder = 2
                    ax.add_patch(cal)

                ci_visible_area = ci_visible_area - intersected_area
            else:
                if sq_intersected is True:
                    intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_x, ci_y, radius)
                    sq_visible_area = sq_visible_area - intersected_area
                    ax.add_patch(square)
                else:
                    intersected_area = du.calculate_intersect_area_ci_ci(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius)
                    ci_left_visible_area = ci_left_visible_area - intersected_area
                    ax.add_patch(cal)
                car.zorder = 2

        ax.add_patch(car)

        # write circle at right
        car_ci_writer.writerow([f'car_{counter}.png', ci_x, ci_y, radius, ci_area, ci_area, ci_dfc, ci_dfc_f, ci_color, bg_color, "Right", "True", variant])

        if do_2_ci is False:
            # write and add square at left
            car_sq_writer.writerow([f'car_{counter}.png', sq_x, sq_y, length, angle, sq_area, sq_visible_area, sq_dfc, sq_dfc_f, corners, sq_color, bg_color, "Left", "False", variant])
            if sq_intersected is False:
                ax.add_patch(square)
        else:
            # write and add circle at left
            car_ci_writer.writerow([f'car_{counter}.png', ci_left_x, ci_left_y, radius, ci_left_area, ci_left_visible_area, ci_left_dfc, ci_left_dfc_f, ci_left_color, bg_color, "Left", "True", variant])
            if ci_intersected is False:
                ax.add_patch(cal)

        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = car_folder_train
        else:
            folder = car_folder_test
        path = os.path.join(folder, f'car_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1

# sar (square at right)
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_length, 150, size)
    do_2_sq = False
    for i in range(size):
        if i >= size / 2:
            do_2_sq = True

        b = f"Generating sar {i+1}/{size} "
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        ax = fig.add_subplot(111, aspect='auto')
        excluded_colors = [bg_color]
        dist_value = distribution[i]
        length = dist_value
        ci_intersected = False
        sq_intersected = False
        if do_2_sq is False:
            # add circle at left
            all_ok = False
            radius = dist_value / 2
            while all_ok is False:
                ci_left_x = np.random.uniform(0 + radius, img_width - radius)
                ci_left_y = np.random.uniform(0 + radius, img_height - radius)

                if du.circle_out_of_bounds(ci_left_x, ci_left_y, radius, img_width, img_height):
                    continue

                if du.circle_is_at_right(ci_left_x, radius, img_width):
                    continue

                all_ok = True

            ci_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(ci_left_color)
            ci_left_dfc = du.calculate_dfc_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_dfc_f = du.calculate_dfc_further_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_area = round(np.pi * radius ** 2, 2)
            ci_left_visible_area = ci_left_area
            cal = patches.Circle((ci_left_x, ci_left_y), radius, color=ci_left_color)

        else:
            # add square at left
            all_ok = False
            while all_ok is False:
                sq_left_x = np.random.uniform(0, img_width - length)
                sq_left_y = np.random.uniform(0, img_height - length)
                sq_left_angle = np.random.uniform(0, 360)
                sq_left_center_x = sq_left_x + length / 2
                sq_left_center_y = sq_left_y + length / 2

                left_square = patches.Rectangle((sq_left_x, sq_left_y), length, length, angle=sq_left_angle, rotation_point=(sq_left_center_x, sq_left_center_y))
                left_corners = left_square.get_corners()

                if du.square_out_of_bounds(left_corners, img_width, img_height) is True:
                    continue

                if du.square_is_at_right(left_corners, img_width, img_height) is True:
                    continue

                all_ok = True

            sq_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(sq_left_color)
            sq_left_dfc = du.calculate_dfc_square(sq_left_x, sq_left_y, length, sq_left_angle, img_width, img_height)
            sq_left_dfc_f = du.calculate_dfc_further_square(sq_left_x, sq_left_y, length, sq_left_angle, img_width, img_height)
            sq_left_area = round(length ** 2, 2)
            sq_left_visible_area = sq_left_area
            left_square.set_color(sq_left_color)

        all_ok = False
        while all_ok is False:
            # add the square at right
            sq_x = np.random.uniform(0, img_width - length)
            sq_y = np.random.uniform(0, img_height - length)
            sq_angle = np.random.uniform(0, 360)
            sq_center_x = sq_x + length / 2
            sq_center_y = sq_y + length / 2

            square = patches.Rectangle((sq_x, sq_y), length, length, angle=sq_angle, rotation_point=(sq_center_x, sq_center_y))
            corners = square.get_corners()

            if du.square_out_of_bounds(corners, img_width, img_height) is True:
                continue

            if du.square_is_at_right(corners, img_width, img_height) is False:
                continue

            repeat = False
            if do_2_sq is False:
                # check if the square is more to the right than the circle
                sqar = False
                for corner in corners:
                    if corner[0] <= (ci_left_x - radius):
                        reapeat = True
                        break
            else:
                # check if the square is more to the right than the square
                sqar = False
                corner_count = 0
                for corner in corners:
                    for left_corner in left_corners:
                        if corner[0] <= left_corner[0]:
                            corner_count += 1

                if corner_count == 4:
                    reapeat = True

            if repeat is True:
                continue

            # check overlaps
            if do_2_sq is False:
                if du.circle_intersect_square(ci_left_x, ci_left_y, radius, corners) is True:
                    sq_intersected = True
            else:
                if du.square_overlap(corners, left_corners) is True:
                    ci_intersected = True

            all_ok = True

        sq_color = du.generate_nonmatching_color(excluded_colors)
        excluded_colors.append(sq_color)
        square.set_color(sq_color)
        sq_dfc = du.calculate_dfc_square(sq_x, sq_y, length, sq_angle, img_width, img_height)
        sq_dfc_f = du.calculate_dfc_further_square(sq_x, sq_y, length, sq_angle, img_width, img_height)
        sq_area = round(length ** 2, 2)
        sq_visible_area = sq_area

        # handle intersected visible areas
        if sq_intersected is True or ci_intersected is True:
            # decide if square is under or above the circle
            put_square_under = np.random.choice([True, False])
            if put_square_under is True:
                if sq_intersected is True:
                    intersected_area = du.calculate_intersect_area_sq_sq(corners, left_corners)
                    left_square.zorder = 2
                    ax.add_patch(left_square)
                else:
                    intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_left_x, ci_left_y, radius)
                    cal.zorder = 2
                    ax.add_patch(cal)

                sq_visible_area = sq_visible_area - intersected_area
            else:
                # print(counter)
                if sq_intersected is True:
                    intersected_area = du.calculate_intersect_area_sq_sq(corners, left_corners)
                    sq_left_visible_area = sq_left_visible_area - intersected_area
                    ax.add_patch(left_square)
                else:
                    intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_left_x, ci_left_y, radius)
                    ci_left_visible_area = ci_left_visible_area - intersected_area
                    ax.add_patch(cal)
                square.zorder = 2

        ax.add_patch(square)

        # write square at right
        sar_sq_writer.writerow([f'sar_{counter}.png', sq_x, sq_y, length, sq_angle, sq_area, sq_visible_area, sq_dfc, sq_dfc_f, corners, sq_color, bg_color, "Right", "False", variant])

        if do_2_sq is False:
            # write and add circle at left
            sar_ci_writer.writerow([f'sar_{counter}.png', ci_left_x, ci_left_y, radius, ci_left_area, ci_left_visible_area, ci_left_dfc, ci_left_dfc_f, ci_left_color, bg_color, "Left", "True", variant])
            if ci_intersected is False:
                ax.add_patch(cal)
        else:
            # write and add square at left
            sar_sq_writer.writerow([f'sar_{counter}.png', sq_left_x, sq_left_y, length, sq_left_angle, sq_left_area, sq_left_visible_area, sq_left_dfc, sq_left_dfc_f, left_corners, sq_left_color, bg_color, "Left", "False", variant])
            if sq_intersected is False:
                ax.add_patch(left_square)

        fig.set_facecolor(bg_color)
        ax.set_xlim(0, img_width)
        ax.set_ylim(0, img_height)
        ax.axis('off')
        if j == 0:
            folder = sar_folder_train
        else:
            folder = sar_folder_test
        path = os.path.join(folder, f'sar_{counter}.png')
        plt.savefig(path, bbox_inches=None, pad_inches=0, dpi=100)
        plt.clf()
        counter += 1
