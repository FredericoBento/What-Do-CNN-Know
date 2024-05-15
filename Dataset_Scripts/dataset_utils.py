import numpy as np
import math
from shapely import geometry
from shapely import affinity
from variables import *


def cornerOutOfBounds(x, y, width, height):
    if x < 5:
        return True
    if x > width:
        return True

    if y < 5:
        return True
    if y > height:
        return True

    return False


def calc_triangle_side_for_area(area):
     # Generate a random base within the range of valid bases for the given area
    base = np.random.uniform(10, 1000)

    # Calculate the corresponding height for the given area and base
    height = (2 * area) / base

    # Generate a random side within the range of valid sides for the given area and height
    side = np.random.uniform(10, (2 * area) / height)

    # Generate another random side within the same range
    side2 = np.random.uniform(10, (2 * area) / height)

    # Ensure that the sum of any two sides is greater than the third side
    while side + side2 <= base or side + base <= side2 or base + side2 <= side:
        side2 = np.random.uniform(10, (2 * area) / height)

    return side, side2, base


def random_triangle():
    s1 = np.random.uniform(min_triangle_length, max_triangle_length)
    s2 = np.random.uniform(min_triangle_length, max_triangle_length)
    s3 = np.random.uniform(min_triangle_length, max_triangle_length)

    while s1 + s2 <= s3 or s1 + s3 <= s2 or s2 + s3 <= s1:
        s1 = np.random.uniform(min_triangle_length, max_triangle_length)
        s2 = np.random.uniform(min_triangle_length, max_triangle_length)
        s3 = np.random.uniform(min_triangle_length, max_triangle_length)

    base = s3
    if s1 > s2 and s1 > s3:
        base = s1
        s1 = s3
    elif s2 > s1 and s2 > s3:
        base = s2
        s2 = s3

    return s1, s2, base

def triangle_out_of_bounds(corners, img_width, img_height):
    if cornerOutOfBounds(corners[0][0], corners[0][1], img_width, img_height) or \
        cornerOutOfBounds(corners[1][0], corners[1][1], img_width, img_height) or \
            cornerOutOfBounds(corners[2][0], corners[2][1], img_width, img_height):
        return True


a = 1

def get_triangle_corners(x, y, s1, s2, base, angle):
    half_base = base / 2
    height = math.sqrt(max(0, s1**2 - (half_base)**2))

    # Calculate the coordinates of the left and right corners
    left_corner_x = x - half_base
    right_corner_x = x + half_base
    left_corner_y = right_corner_y = y + (s2 / 2)  # Assuming the center is at the midpoint of the base

    # Calculate the coordinates of the rotated top corner relative to the center
    rotated_top_x = height * math.cos(math.radians(angle))
    rotated_top_y = height * math.sin(math.radians(angle))


    # Calculate the absolute coordinates of the top corner after rotation
    top_corner_x = x + rotated_top_x
    top_corner_y = y + rotated_top_y

    if height < min_triangle_length * 2:
        return None

    lc = affinity.rotate(geometry.Point(left_corner_x, left_corner_y), angle, origin=geometry.Point(x, y))
    rc = affinity.rotate(geometry.Point(right_corner_x, right_corner_y), angle, origin=geometry.Point(x, y))
    tc = affinity.rotate(geometry.Point(top_corner_x, top_corner_y), angle, origin=geometry.Point(x, y))

    return [(lc.x, lc.y), (rc.x, rc.y), (tc.x, tc.y)]
    # return [(left_corner_x, left_corner_y), (right_corner_x, right_corner_y), (top_corner_x, top_corner_y)]



def calculate_dfc_triangle(corners, img_width, img_height):
    center_image = geometry.Point(img_width/2, img_height/2)
    triangle = geometry.Polygon(corners)
    dfc = center_image.distance(triangle)
    return round(dfc, 2)


def get_triangle_area(corners):
    triangle = geometry.Polygon(corners)
    return round(triangle.area, 2)


def calculate_dfc_further_triangle(corners, img_width, img_height):
    center_image = geometry.Point(img_width/2, img_height/2)
    triangle = geometry.Polygon(corners)
    corners = triangle.exterior.coords
    further_corner = corners[0]
    for corner in corners:
        if center_image.distance(geometry.Point(corner)) > center_image.distance(geometry.Point(further_corner)):
            further_corner = corner
    dfc = center_image.distance(geometry.Point(further_corner))
    return round(dfc, 2)


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


def get_square_corners(x, y, length, angle):
    corners = [(x, y), (x + length, y), (x + length, y + length), (x, y + length)]
    # apply rotation
    corners = affinity.rotate(geometry.Polygon(corners), angle).exterior.coords
    return [(corners[0][0], corners[0][1]), (corners[1][0], corners[1][1]), (corners[2][0], corners[2][1]), (corners[3][0], corners[3][1])]


def square_is_at_right(corners, width, height):
    # Check if the square is at the right
    if corners[0][0] > width / 2 and corners[1][0] > width / 2 and corners[2][0] > width / 2 and corners[3][0] > width / 2:
        return True
    return False


def circle_is_at_right(x, radius, width):
    # Check if the circle is at the right
    if x + radius > width / 2:
        return True
    return False


def square_overlap(corners, other_corners):
    shape1 = geometry.Polygon(corners)
    shape2 = geometry.Polygon(other_corners)
    return shape1.intersects(shape2)


def calculate_visible_area_square(x, y, length, angle, image_width, image_height):
    total_visible_area = 0.00
    border = geometry.Polygon([(0, 0), (image_width, 0), (image_width, image_height), (0, image_height)])
    square = geometry.Polygon([(x, y), (x + length, y), (x + length, y + length), (x, y + length)])
    square = affinity.rotate(square, angle)

    if border.contains(square):
        total_visible_area = square.area
    elif border.intersects(square):
        total_visible_area = square.intersection(border).area

    return round(total_visible_area, 2)


def calculate_intersect_area_sq_ci(corners, x, y, radius):
    square = geometry.Polygon(corners)
    circle = geometry.Point(x, y).buffer(radius, resolution=120)
    return round(square.intersection(circle).area, 2)


def calculate_intersect_area_sq_sq(corners, corners2):
    square1 = geometry.Polygon(corners)
    square2 = geometry.Polygon(corners2)
    return round(square1.intersection(square2).area, 2)


def calculate_intersect_area_ci_ci(x, y, radius, x2, y2, radius2):
    circle1 = geometry.Point(x, y).buffer(radius, resolution=120)
    circle2 = geometry.Point(x2, y2).buffer(radius2, resolution=120)
    return round(circle1.intersection(circle2).area, 2)


def calculate_visible_area_circle(x, y, radius, image_width, image_height):
    visible_area = 0
    circle = geometry.Point(x, y).buffer(radius, resolution=120)
    border = geometry.Polygon([(0, 0), (image_width, 0), (image_width, image_height), (0, image_height)])

    if border.contains(circle):
        visible_area = circle.area
    elif border.intersects(circle):
        visible_area = circle.intersection(border).area

    return round(visible_area, 2)


def calculate_dfc_square(x, y, length, angle, image_width, image_height):
    center_image = geometry.Point(image_width/2, image_height/2)
    square = geometry.Polygon([(x, y), (x + length, y), (x + length, y + length), (x, y + length)])
    square = affinity.rotate(square, angle)
    dfc = center_image.distance(square)

    return round(dfc, 2)


def calculate_dfc_further_square(x, y, length, angle, image_width, image_height):
    center_image = geometry.Point(image_width/2, image_height/2)
    square = geometry.Polygon([(x, y), (x + length, y), (x + length, y + length), (x, y + length)])
    square = affinity.rotate(square, angle)
    corners = square.exterior.coords
    further_corner = corners[0]
    for corner in corners:
        if center_image.distance(geometry.Point(corner)) > center_image.distance(geometry.Point(further_corner)):
            further_corner = corner

    # f = furthest_point_of_square([(x, y), (x + length, y), (x + length, y + length), (x, y + length)], (image_width/2, image_height/2))

    dfc = center_image.distance(geometry.Point(further_corner))
    return round(dfc, 2)


def furthest_point_of_square(square_vertices, point):
    max_distance = 0
    furthest_point = None
    # Iterate over each edge of the square

    for i in range(len(square_vertices)):
        x1, y1 = square_vertices[i]
        x2, y2 = square_vertices[(i + 1) % len(square_vertices)]  # Next vertex, handling wrap-around

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        m_point = (point[1] - center_y) / (point[0] - center_x)
        c_point = point[1] - m_point * point[0]

        # Calculate the equation of the line for the current edge
        if x2 - x1 == 0:  # Check if the line is vertical to avoid division by zero
            m = float('inf')  # Set slope to infinity for a vertical line
            intersection_x = x1  # x-coordinate of the intersection is the x-intercept
            intersection_y = m_point * intersection_x + c_point  # Use given point's equation to find y-coordinate
        else:
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            # Calculate the intersection point of the two lines
            intersection_x = (c_point - c) / (m - m_point)
            intersection_y = m * intersection_x + c

        # Check if the intersection point is within the range of the current edge
        if min(x1, x2) <= intersection_x <= max(x1, x2) and min(y1, y2) <= intersection_y <= max(y1, y2):
            # Calculate the distance from the given point to the intersection point
            dist = geometry.Point(point).distance(geometry.Point(intersection_x, intersection_y))
            if dist > max_distance:
                max_distance = dist
                furthest_point = (intersection_x, intersection_y)

    return furthest_point


def calculate_dfc_further_circle(x, y, radius, image_width, image_height):
    distance = calculate_dfc_circle(x, y, radius, image_width, image_height)
    dfc_further = distance + (radius*2)
    return round(dfc_further, 2)


def calculate_dfc_circle(x, y, radius, image_width, image_height):
    center_image = geometry.Point(image_width/2, image_height/2)
    circle = geometry.Point(x, y).buffer(radius, resolution=120)
    dfc = center_image.distance(circle)
    return round(dfc, 2)


def circle_overlap(x1, y1, r1, x2, y2, r2):
    shape = geometry.Point(x1, y1).buffer(r1, resolution=120)
    other_shape = geometry.Point(x2, y2).buffer(r2, resolution=120)
    return shape.intersects(other_shape)


def circle_intersect_circle(x1, y1, r1, x2, y2, r2):
    return circle_overlap(x1, y1, r1, x2, y2, r1)


def square_intersect_square(corners, corners2):
    return square_overlap(corners, corners2)


def square_intersect_circle(corners, x, y, radius):
    shape1 = geometry.Polygon(corners)
    shape2 = geometry.Point(x, y).buffer(radius, resolution=120)
    return shape1.intersects(shape2)


def circle_intersect_square(x, y, radius, corners):
    return square_intersect_circle(corners, x, y, radius)


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
