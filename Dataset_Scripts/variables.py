import numpy as np

train_size = int(300 / 3)
test_size = int(60 / 3)

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

min_triangle_length = 20
max_triangle_length = img_width / 2

min_triangle_area = 0.5 * min_triangle_length ** 2
max_triangle_area = 0.5 * max_triangle_length ** 2

outside_min = 45
