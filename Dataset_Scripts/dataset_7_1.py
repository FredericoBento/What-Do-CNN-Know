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
                        'Distance From Center Further', 'Color', 'Bg_color', 'Position', 'Intersected', 'Cut', 'Variant'])

sar_sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Distance From Center'
                        , 'Distance From Center Further',
                        'Corners', 'Color', 'Bg_color', 'Position', 'Intersected', 'Cut', 'Variant'])

car_sq_writer = csv.writer(open(os.path.join(data_folder, 'car_sq.csv'), 'w'))
car_ci_writer = csv.writer(open(os.path.join(data_folder, 'car_ci.csv'), 'w'))
car_ci_writer.writerow(['Filename', 'X', 'Y', 'Radius', 'Area', 'Visible Area', 'Distance From Center',
                        'Distance From Center Further', 'Color', 'Bg_color', 'Position', 'Intersected', 'Cut', 'Variant'])

car_sq_writer.writerow(['Filename', 'X', 'Y', 'Length', 'Angle', 'Area', 'Visible Area', 'Distance From Center'
                        , 'Distance From Center Further',
                        'Corners', 'Color', 'Bg_color', 'Position', 'Intersected', 'Cut', 'Variant'])

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

    distribution = np.random.uniform(min_square_length, 150, int(size / 8))
    dist_idx = 0
    do_2_ci = False
    put_circle_under = False
    intersection_counter_reached = False
    img_counter = 0
    # for i in range(size):
    while counter <= size:
        i = counter -1
        if img_counter >= size / 8 and put_circle_under is False:
            # change the position of the circle
            put_circle_under = True
            distribution = np.random.uniform(min_square_length, 150, int(size / 8))
            dist_idx = 0

        if img_counter >= size / 4 and intersection_counter_reached is False:
            # stop intersections
            intersection_counter_reached = True
            distribution = np.random.uniform(min_square_length, 150, int(size / 4))
            dist_idx = 0

        if img_counter >= size / 2 and do_2_ci is False:
            # change combination
            do_2_ci = True
            intersection_counter_reached = False
            put_circle_under = False
            distribution = np.random.uniform(min_square_length, 150, int(size / 8))
            dist_idx = 0
            img_counter = 0

        b = f"Generating car {i+1}/{size} "
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        ax = fig.add_subplot(111, aspect='auto')
        excluded_colors = [bg_color]
        if dist_idx >= len(distribution):
            dist_idx -= 1
        dist_value = distribution[dist_idx]
        radius = dist_value / 2
        sq_intersected = False
        ci_intersected = False
        if do_2_ci is False:
            # add square at left
            length = dist_value
            all_ok = False
            while all_ok is False:
                sq_x = np.random.uniform(0, img_width - length - 20)
                sq_y = np.random.uniform(0, img_height - length - 20)
                angle = np.random.uniform(0, 360)
                sq_center_x = sq_x + length / 2
                sq_center_y = sq_y + length / 2

                square = patches.Rectangle((sq_x, sq_y), length, length, angle=angle, rotation_point=(sq_center_x, sq_center_y))
                corners = square.get_corners()

                if du.square_out_of_bounds(corners, img_width, img_height) is True:
                    continue

                all_ok = True

            sq_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(sq_color)
            square.set_color(sq_color)
            sq_dfc = du.calculate_dfc_square(sq_x, sq_y, length, angle, img_width, img_height)
            sq_dfc_f = du.calculate_dfc_further_square(sq_x, sq_y, length, angle, img_width, img_height)
            sq_area = round(length ** 2, 2)
            sq_visible_area = du.calculate_visible_area_square(sq_x, sq_y, length, angle, img_width, img_height)
            sq_cut = du.square_is_cut(corners, img_width, img_height)

        else:
            # add circle at left
            all_ok = False
            while all_ok is False:
                ci_left_x = np.random.uniform(0 + radius, img_width - radius - 20)
                ci_left_y = np.random.uniform(0 + radius, img_height - radius - 20)

                if du.circle_out_of_bounds(ci_left_x, ci_left_y, radius, img_width, img_height) is True:
                    continue

                all_ok = True

            ci_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(ci_left_color)
            ci_left_dfc = du.calculate_dfc_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_dfc_f = du.calculate_dfc_further_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_area = round(np.pi * radius ** 2, 2)
            cal = patches.Circle((ci_left_x, ci_left_y), radius, color=ci_left_color)
            ci_left_visible_area = du.calculate_visible_area_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_cut = du.circle_is_cut(ci_left_x, ci_left_y, radius, img_width, img_height)

        all_ok = False
        anti_intersect_block = False
        tries = 0
        max_tries = 100
        while all_ok is False:
            # add the circle at right
            if tries >= max_tries:
                anti_intersect_block = True
                break

            if intersection_counter_reached is False:
                # force intersection
                intersect = False
                if do_2_ci is False:
                    while intersect is False:
                        diagonal = np.sqrt(length ** 2 + length **2)
                        ci_x = np.random.uniform(sq_center_x - diagonal, sq_center_x + diagonal)
                        ci_y = np.random.uniform(sq_y - diagonal, sq_y + diagonal)
                        intersect = du.circle_intersect_square(ci_x, ci_y, radius, corners)
                else:
                    while intersect is False:
                        ci_x = np.random.uniform(ci_left_x - radius, ci_left_x + radius)
                        ci_y = np.random.uniform(ci_left_y - radius, ci_left_y + radius)
                        intersect = du.circle_intersect_circle(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius)
            else:
                ci_x = np.random.uniform(0 + radius, img_width - radius)
                ci_y = np.random.uniform(0 + radius, img_height - radius)

            if du.circle_out_of_bounds(ci_x, ci_y, radius, img_width, img_height) is True:
                continue

            # check if square or circle is more to the right
            repeat = False
            if do_2_ci is False:
                for corner in corners:
                    if (ci_x + radius) <= corner[0]:
                        repeat = True
                        break
            else:
                if ci_x + radius <= (ci_left_x + radius):
                    repeat = True

            if repeat is True:
                continue

            # check if there was intersections
            if do_2_ci is False:
                if du.circle_intersect_square(ci_x, ci_y, radius, corners) is True:
                    sq_intersected = True
            else:
                if du.circle_intersect_circle(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius) is True:
                    ci_intersected = True

            all_ok = True
            if sq_intersected is True or ci_intersected is True:
                if intersection_counter_reached is True:
                    all_ok = False
                    tries += 1

        if anti_intersect_block is False:
            ci_color = du.generate_nonmatching_color(excluded_colors)
            ci_dfc = du.calculate_dfc_circle(ci_x, ci_y, radius, img_width, img_height)
            ci_dfc_f = du.calculate_dfc_further_circle(ci_x, ci_y, radius, img_width, img_height)
            ci_area = round(np.pi * radius ** 2, 2)
            ci_visible_area = du.calculate_visible_area_circle(ci_x, ci_y, radius, img_width, img_height)
            car = patches.Circle((ci_x, ci_y), radius, color=ci_color)
            ci_cut = du.circle_is_cut(ci_x, ci_y, radius, img_width, img_height)

            # handle intersected visible areas
            can_continue = True
            if sq_intersected is True or ci_intersected is True:
                # decide if circle is under or above
                if put_circle_under is True:
                    if sq_intersected is True:
                        intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_x, ci_y, radius)
                        square.set_color(sq_color)
                        square.zorder = 2
                        ax.add_patch(square)
                    else:
                        intersected_area = du.calculate_intersect_area_ci_ci(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius)
                        cal.zorder = 2
                        ax.add_patch(cal)

                    ci_visible_area = round(ci_visible_area - intersected_area, 2)
                    if ci_visible_area <= 0:
                        can_continue = False
                else:
                    if sq_intersected is True:
                        intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_x, ci_y, radius)
                        sq_visible_area = round(sq_visible_area - intersected_area, 2)
                        ax.add_patch(square)
                        ci_visible_area = ci_area
                        if sq_visible_area <= 0:
                            can_continue = False
                    else:
                        intersected_area = du.calculate_intersect_area_ci_ci(ci_x, ci_y, radius, ci_left_x, ci_left_y, radius)
                        ci_left_visible_area = round(ci_left_visible_area - intersected_area, 2)
                        ax.add_patch(cal)
                        if ci_left_visible_area <= 0:
                            can_continue = False
                    car.zorder = 2

            if can_continue is False:
                plt.clf()
                break

            ax.add_patch(car)

            intersected = not intersection_counter_reached

            # write circle at right
            car_ci_writer.writerow([f'car_{counter}.png', ci_x, ci_y, radius, ci_area, ci_visible_area, ci_dfc, ci_dfc_f, ci_color, bg_color, "Right", intersected, ci_cut, variant])

            if do_2_ci is False:
                # write and add square at left
                car_sq_writer.writerow([f'car_{counter}.png', sq_x, sq_y, length, angle, sq_area, sq_visible_area, sq_dfc, sq_dfc_f, corners, sq_color, bg_color, "Left", intersected, sq_cut, variant])
                if sq_intersected is False:
                    ax.add_patch(square)
            else:
                # write and add circle at left
                car_ci_writer.writerow([f'car_{counter}.png', ci_left_x, ci_left_y, radius, ci_left_area, ci_left_visible_area, ci_left_dfc, ci_left_dfc_f, ci_left_color, bg_color, "Left", intersected, ci_left_cut, variant])
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
            counter += 1
            img_counter += 1

        dist_idx += 1
        plt.clf()

# sar (square at right)
counter = 1
for j in range(2):
    if j == 0:
        variant = 'Train'
        size = train_size
    else:
        variant = 'Test'
        size = test_size

    distribution = np.random.uniform(min_square_length, 150, int(size / 8))
    dist_idx = 0
    do_2_sq = False
    put_square_under = False
    intersection_counter_reached = False
    img_counter = 0
    for i in range(size):
        i = counter - 1
        if img_counter >= size / 8 and put_square_under is False:
            # change the position of the circle
            put_square_under = True
            distribution = np.random.uniform(min_square_length, 150, int(size / 8))
            dist_idx = 0

        if img_counter >= size / 4 and intersection_counter_reached is False:
            # stop intersections
            intersection_counter_reached = True
            distribution = np.random.uniform(min_square_length, 150, int(size / 4))
            dist_idx = 0

        if img_counter >= size / 2 and do_2_sq is False:
            # change combination
            do_2_sq = True
            intersection_counter_reached = False
            put_square_under = False
            distribution = np.random.uniform(min_square_length, 150, int(size / 8))
            dist_idx = 0
            img_counter = 0


        b = f"Generating sar {i+1}/{size} "
        print(b, end='\r', flush=True)
        bg_color = du.generate_nonmatching_color()
        ax = fig.add_subplot(111, aspect='auto')
        excluded_colors = [bg_color]
        if dist_idx >= len(distribution):
            dist_idx -= 1
        dist_value = distribution[dist_idx]
        length = dist_value
        ci_intersected = False
        sq_intersected = False
        if do_2_sq is False:
            # add circle at left
            all_ok = False
            radius = dist_value / 2
            while all_ok is False:
                ci_left_x = np.random.uniform(0 + radius, img_width - radius - 20)
                ci_left_y = np.random.uniform(0 + radius, img_height - radius - 20)

                if du.circle_out_of_bounds(ci_left_x, ci_left_y, radius, img_width, img_height):
                    continue

                all_ok = True

            ci_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(ci_left_color)
            ci_left_dfc = du.calculate_dfc_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_dfc_f = du.calculate_dfc_further_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_area = round(np.pi * radius ** 2, 2)
            cal = patches.Circle((ci_left_x, ci_left_y), radius, color=ci_left_color)
            ci_left_visible_area = du.calculate_visible_area_circle(ci_left_x, ci_left_y, radius, img_width, img_height)
            ci_left_cut = du.circle_is_cut(ci_left_x, ci_left_y, radius, img_width, img_height)

        else:
            # add square at left
            all_ok = False
            while all_ok is False:
                # sq_left_x = np.random.uniform(0, img_width - length)
                sq_left_x = np.random.uniform(0, img_width - length - 20)
                sq_left_y = np.random.uniform(0, img_height - length - 20)
                sq_left_angle = np.random.uniform(0, 360)
                sq_left_center_x = sq_left_x + length / 2
                sq_left_center_y = sq_left_y + length / 2

                left_square = patches.Rectangle((sq_left_x, sq_left_y), length, length, angle=sq_left_angle, rotation_point=(sq_left_center_x, sq_left_center_y))
                left_corners = left_square.get_corners()

                if du.square_out_of_bounds(left_corners, img_width, img_height) is True:
                    continue

                all_ok = True

            sq_left_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(sq_left_color)
            left_square.set_color(sq_left_color)
            sq_left_dfc = du.calculate_dfc_square(sq_left_x, sq_left_y, length, sq_left_angle, img_width, img_height)
            sq_left_dfc_f = du.calculate_dfc_further_square(sq_left_x, sq_left_y, length, sq_left_angle, img_width, img_height)
            sq_left_area = round(length ** 2, 2)
            sq_left_visible_area = du.calculate_visible_area_square(sq_left_x, sq_left_y, length, sq_left_angle, img_width, img_height)
            sq_left_cut = du.square_is_cut(left_corners, img_width, img_height)

        all_ok = False
        anti_intersect_block = False
        tries = 0
        max_tries = 100
        while all_ok is False:
            if tries >= max_tries:
                anti_intersect_block = True
                break

            if intersection_counter_reached is False:
                # force intersection
                intersect = False
                if do_2_sq is False:
                    while intersect is False:
                        sq_x = np.random.uniform(ci_left_x - radius, ci_left_x + radius)
                        sq_y = np.random.uniform(ci_left_y - radius, ci_left_y + radius)
                        sq_angle = np.random.uniform(0, 360)
                        sq_center_x = sq_x + length / 2
                        sq_center_y = sq_y + length / 2
                        square = patches.Rectangle((sq_x, sq_y), length, length, angle=sq_angle, rotation_point=(sq_center_x, sq_center_y))
                        corners = square.get_corners()
                        intersect = du.circle_intersect_square(ci_left_x, ci_left_y, radius, corners)
                else:
                    while intersect is False:
                        diagonal = np.sqrt(length ** 2 + length ** 2)
                        sq_x = np.random.uniform(sq_left_x, sq_left_x + diagonal)
                        sq_y = np.random.uniform(sq_left_y, sq_left_y + diagonal)
                        sq_angle = np.random.uniform(0, 360)
                        sq_center_x = sq_x + length / 2
                        sq_center_y = sq_y + length / 2
                        square = patches.Rectangle((sq_x, sq_y), length, length, angle=sq_angle, rotation_point=(sq_center_x, sq_center_y))
                        corners = square.get_corners()
                        intersect = du.square_intersect_square(corners, left_corners)
            else:
                sq_x = np.random.uniform(0, img_width - length)
                sq_y = np.random.uniform(0, img_height - length)
                sq_angle = np.random.uniform(0, 360)
                sq_center_x = sq_x + length / 2
                sq_center_y = sq_y + length / 2
                square = patches.Rectangle((sq_x, sq_y), length, length, angle=sq_angle, rotation_point=(sq_center_x, sq_center_y))
                corners = square.get_corners()

            if du.square_out_of_bounds(corners, img_width, img_height) is True:
                continue

            # check if square is more to the right
            repeat = False
            count = 0
            if do_2_sq is False:
                for corner in corners:
                    if corner[0] <= (ci_left_x + radius):
                        count += 1

                if count == 4:
                    repeat = True
            else:
                # check if the square is more to the right than the square
                corner_count = 0
                for corner in corners:
                    for left_corner in left_corners:
                        if corner[0] <= left_corner[0]:
                            corner_count += 1

                if corner_count == 4:
                    repeat = True

                if counter == 56:
                    print(repeat, corner_count)

            if repeat is True:
                continue

            # check overlaps
            if do_2_sq is False:
                if du.circle_intersect_square(ci_left_x, ci_left_y, radius, corners) is True:
                    ci_intersected = True
            else:
                if du.square_intersect_square(corners, left_corners) is True:
                    sq_intersected = True

            all_ok = True
            if sq_intersected is True or ci_intersected is True:
                if intersection_counter_reached is True:
                    all_ok = False
                    tries += 1

        if anti_intersect_block is False:
            sq_color = du.generate_nonmatching_color(excluded_colors)
            excluded_colors.append(sq_color)
            square.set_color(sq_color)
            sq_dfc = du.calculate_dfc_square(sq_x, sq_y, length, sq_angle, img_width, img_height)
            sq_dfc_f = du.calculate_dfc_further_square(sq_x, sq_y, length, sq_angle, img_width, img_height)
            sq_area = round(length ** 2, 2)
            sq_visible_area = sq_area

            # handle intersected visible areas
            can_continue = True
            if sq_intersected is True or ci_intersected is True:
                # decide if square is under or above the circle
                if put_square_under is True:
                    if sq_intersected is True:
                        intersected_area = du.calculate_intersect_area_sq_sq(corners, left_corners)
                        left_square.zorder = 2
                        ax.add_patch(left_square)
                    else:
                        intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_left_x, ci_left_y, radius)
                        cal.zorder = 2
                        ax.add_patch(cal)

                    sq_visible_area = round(sq_visible_area - intersected_area, 2)
                    if sq_visible_area <= 0:
                        can_continue = False
                else:
                    if sq_intersected is True:
                        intersected_area = du.calculate_intersect_area_sq_sq(corners, left_corners)
                        sq_left_visible_area = round(sq_left_visible_area - intersected_area, 2)
                        ax.add_patch(left_square)
                        sq_visible_area = sq_area
                        if sq_visible_area <= 0:
                            can_continue = False
                    else:
                        intersected_area = du.calculate_intersect_area_sq_ci(corners, ci_left_x, ci_left_y, radius)
                        ci_left_visible_area = round(ci_left_visible_area - intersected_area, 2)
                        ax.add_patch(cal)
                        if ci_left_visible_area <= 0:
                            can_continue = False
                    square.zorder = 2

            if can_continue is False:
                plt.clf()
                break

            ax.add_patch(square)
            intersected = not intersection_counter_reached

            # write square at right
            sar_sq_writer.writerow([f'sar_{counter}.png', sq_x, sq_y, length, sq_angle, sq_area, sq_visible_area, sq_dfc, sq_dfc_f, corners, sq_color, bg_color, "Right", intersected, sq_cut, variant])

            if do_2_sq is False:
                # write and add circle at left
                sar_ci_writer.writerow([f'sar_{counter}.png', ci_left_x, ci_left_y, radius, ci_left_area, ci_left_visible_area, ci_left_dfc, ci_left_dfc_f, ci_left_color, bg_color, "Left", intersected, ci_left_cut, variant])
                if ci_intersected is False:
                    ax.add_patch(cal)
            else:
                # write and add square at left
                sar_sq_writer.writerow([f'sar_{counter}.png', sq_left_x, sq_left_y, length, sq_left_angle, sq_left_area, sq_left_visible_area, sq_left_dfc, sq_left_dfc_f, left_corners, sq_left_color, bg_color, "Left", intersected, sq_left_cut, variant])
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
            counter += 1
            img_counter += 1

        dist_idx += 1
        plt.clf()

# 100
# 	CI SQ (50)
# 		- 13 COM INT ABOVE
# 		- 13 com INT UNDER
# 		- 25 SEM INT
# 		
# 	CI CI (50)
# 		- 13 COM INT ABOVE
# 		- 13 COM INT UNDER
# 		- 25 SEM INT
