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

