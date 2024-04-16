import numpy as np
import shapely.geometry as geometry


def cornerOutOfBounds(x, y, width, height):
    if x < 0:
        return True
    if x > width:
        return True

    if y < 0:
        return True
    if y > height:
        return True

    return False


def square_out_of_bounds(corners, width, height):
    if cornerOutOfBounds(corners[0][0], corners[0][1], width, height) or \
        cornerOutOfBounds(corners[1][0], corners[1][1], width, height) or \
        cornerOutOfBounds(corners[2][0], corners[2][1], width, height) or \
            cornerOutOfBounds(corners[3][0], corners[3][1], width, height):
        return True
    return False


def square_is_cut(corners, width, height):
    if square_out_of_bounds(corners, width, height) is False:
        return False

    corners_outside = 0
    if corners[0][0] < 0 or corners[0][0] > width or corners[0][1] < 0 or corners[0][1] > height:
        corners_outside += 1
    if corners[1][0] < 0 or corners[1][0] > width or corners[1][1] < 0 or corners[1][1] > height:
        corners_outside += 1
    if corners[2][0] < 0 or corners[2][0] > width or corners[2][1] < 0 or corners[2][1] > height:
        corners_outside += 1
    if corners[3][0] < 0 or corners[3][0] > width or corners[3][1] < 0 or corners[3][1] > height:
        corners_outside += 1

    if corners_outside >= 3:
        return False

    return True


def square_overlap(corners, other_corners):
    shape1 = geometry.Polygon(corners)
    shape2 = geometry.Polygon(other_corners)
    return shape1.intersects(shape2)


def calculate_visible_area(x, y, length, image_width, image_height):
    total_visible_area = 0
    for i in range(len(x)):
        # Calculate the coordinates of the visible rectangle
        x1 = max(x[i], 0)
        y1 = max(y[i], 0)
        x2 = min(x[i] + length[i], image_width)
        y2 = min(y[i] + length[i], image_height)

        # Calculate the width and height of the visible rectangle
        width = x2 - x1
        height = y2 - y1

        # If any part of the square is within the image boundaries
        if width > 0 and height > 0:
            # Calculate the area of the visible portion
            visible_area = width * height
            total_visible_area += visible_area

    return total_visible_area


def calculate_visible_area_circle(x, y, radius, image_width, image_height):
    # Calculate the bounding box of the circle
    x_min = max(x - radius, 0)
    x_max = min(x + radius, image_width)
    y_min = max(y - radius, 0)
    y_max = min(y + radius, image_height)

    # Check if the circle lies completely outside the image boundaries
    if x_min >= image_width or x_max <= 0 or y_min >= image_height or y_max <= 0:
        return 0

    # Calculate area based on the intersection with image boundaries
    area = 0
    if x_min <= 0 and x_max >= image_width and y_min <= 0 and y_max >= image_height:
        # Circle lies completely inside the image boundaries
        area = np.pi * radius**2
    else:
        # Circle partially intersects with image boundaries
        # Calculate the intersection area
        dx = min(x_max, image_width) - max(x_min, 0)
        dy = min(y_max, image_height) - max(y_min, 0)
        area = np.pi * radius**2 * (dx * dy) / (np.pi * radius**2)

    return area


def circle_overlap(x1, y1, r1, x2, y2, r2):
    shape = geometry.Point(x1, y1).buffer(r1)
    other_shape = geometry.Point(x2, y2).buffer(r2)
    return shape.intersects(other_shape)


def circle_is_cut(x, y, radius, width, height):
    if x - radius < 0 or x + radius > width or \
            y - radius < 0 or y + radius > height:
        return True
    return False


def circle_out_of_bounds(x, y, radius, width, height):
    if x - radius < 0 or x + radius > width or \
                y - radius < 0 or y + radius > height:
        return True

    return False


def generate_nonmatching_color(*excluded_colors):
    while True:
        color = np.random.rand(3)
        if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
            return color

