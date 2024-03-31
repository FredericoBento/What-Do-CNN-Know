import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from shapely import geometry
import sys
import os
import matplotlib
from SquareCollection import SquareCollection
from CircleCollection import CircleCollection
from SquareWithCircleCollection import SquareWithCircleCollection

matplotlib.use('TkAgg')


class Generator:
    def __init__(self, image_width=500, image_height=500, seed=None):
        self.num_images = 0
        self.image_width = image_width
        self.image_height = image_height

        self.seed = seed

        self.min_square_side_length = 20
        self.min_circle_radius = 10
        self.max_circle_radius = (image_width / 4) + 15
        self.max_square_side_length = image_width / 2

        self.square_areas_distribution = []
        self.circle_areas_distribution = []

        self.square_collection = SquareCollection(seed=seed)
        self.circle_collection = CircleCollection(seed=seed)
        self.swc_collection = SquareWithCircleCollection(seed=seed)

        if seed is None:
            rand_seed = np.random.randint(0, 1000)
            np.random.seed(rand_seed)
            self.seed = rand_seed
            print(f"Seed not provided. Using random seed {rand_seed}")
        else:
            print(f"Seed provided. Using seed {seed}")
            np.random.seed(seed)

    def generate_images(self, draw_random=False, draw_circle=False, draw_square=False, cut=False, directory="dataset", quantity=1, variant=None):
        if variant is None:
            print("Variant not specified")
            return
        elif variant != "train" and variant != "test":
            print("Invalid variant")
            return
        i = 0
        quantity = int(quantity)
        if draw_random or draw_circle:
            circle_min = self.min_circle_radius**2 * np.pi
            circle_max = self.max_circle_radius**2 * np.pi
            self.circle_areas_distribution = np.random.uniform(circle_min, circle_max, quantity)

        if draw_random or draw_square:
            square_min = self.min_square_side_length**2
            square_max = self.max_square_side_length**2
            self.square_areas_distribution = np.random.uniform(square_min, square_max, quantity)

        figure_width = self.image_width / 100
        figure_height = self.image_height / 100

        print("", flush=True)

        fig = plt.figure(figsize=(figure_width, figure_height), linewidth=0.0)
        while i < quantity:
            b = f"Generating images {i+1}/{quantity}"
            sys.stdout.write('\r'+b)
            if draw_random:
                draw_circle = np.random.choice([True, False])
                draw_square = np.random.choice([True, False])
            bg_color = self._generate_nonmatching_color()
            fig.set_facecolor(bg_color)
            ax = fig.add_subplot(111)
            ax.set_rasterized(True)
            radius = -1
            length = -1
            if draw_square:
                filename = "square_"
                square, shape_square, length = self.make_square(cut=cut, background_color=bg_color, dist_idx=i)

            if draw_circle:
                if draw_square:
                    filename += "circle_"
                else:
                    filename = "circle_"
                circle, shape_circle, radius = self.make_circle(background_color=bg_color, dist_idx=i)

                if draw_square:
                    if shape_square.intersects(shape_circle):
                        while shape_square.intersects(shape_circle):
                            circle, shape_circle, radius = self.make_circle(background_color=bg_color, dist_idx=None)
                            square, shape_square, length = self.make_square(cut=cut, background_color=bg_color, dist_idx=None)

                ax.add_patch(circle)

            if draw_square and length > 0:
                ax.add_patch(square)

            if draw_square and draw_circle:
                c_x, c_y = circle.get_center()
                self.swc_collection.add_square(length, square.angle, square.get_x(), square.get_y(), variant=variant)
                self.swc_collection.add_circle(radius, c_x, c_y, variant=variant)
                self.swc_collection.increase_size(variant)
            elif draw_square:
                self.square_collection.add_square(length, square.angle, square.get_x(), square.get_y(), variant=variant)
            elif draw_circle:
                c_x, c_y = circle.get_center()
                self.circle_collection.add_circle(radius, c_x, c_y, variant=variant)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')

            if draw_square is False and draw_circle is False:
                filename = "none_"

            plt.savefig(f'{directory + "/" + filename + str(i+1)}.png', bbox_inches='tight', pad_inches=0, dpi=106.5)
            plt.clf()

            self.num_images += 1
            i += 1
        plt.close()

    def make_square(self, x=None, y=None, angle=None, length=None, color=None, cut=False, background_color=None, dist_idx=None):
        if color is None:
            color = self._generate_nonmatching_color(background_color)

        if length is None and dist_idx is not None:
            length = np.sqrt(self.square_areas_distribution[dist_idx])

        if dist_idx is None and length is None:
            if len(self.square_areas_distribution) <= 0:
                length = np.random.uniform(self.min_square_side_length, self.max_square_side_length)
            else:
                length = np.random.choice(self.square_areas_distribution)
                length = np.sqrt(length)

        if x is None:
            x = np.random.uniform(0, self.image_width - length)
        if y is None:
            y = np.random.uniform(0, self.image_height - length)
        if angle is None:
            angle = np.random.uniform(0, 360)

        center_x = x + length / 2
        center_y = y + length / 2

        square = Rectangle((x, y), length, length, color=color, angle=angle, rotation_point=(center_x, center_y))
        corners = square.get_corners()

        if cut is True:
            do_again = not self.square_is_cut(corners)
        else:
            do_again = self.square_out_of_bounds(corners)

        max_tries = 5
        max_limit = 100
        tries = 0
        limit_breaker = 0

        while do_again is True:
            if tries >= max_tries:
                length = np.random.choice(self.square_areas_distribution)
                length = np.sqrt(length)
                tries = 0
                limit_breaker += 1

            if limit_breaker >= max_limit:
                print("Max limit reached. Breaking loop")
                print("x=", x, "y=", y, "length=", length, "angle=", angle)
                break

            if cut is False:
                x = np.random.uniform(0, self.image_width - length)
                y = np.random.uniform(0, self.image_height - length)
            else:
                x = np.random.uniform(0-length, self.image_width + length)
                y = np.random.uniform(0-length, self.image_height + length)

            angle = np.random.uniform(0, 360)
            center_x = x + length / 2
            center_y = y + length / 2
            square = Rectangle((x, y), length, length, color=color, angle=angle, rotation_point=(center_x, center_y))
            corners = square.get_corners()

            if cut is False:
                do_again = self.square_out_of_bounds(corners)
            else:
                isCut = self.square_is_cut(corners)
                do_again = not isCut
            tries += 1

        square.set_antialiased(True)
        shape_square = geometry.Polygon(corners)

        return square, shape_square, length

    def square_out_of_bounds(self, corners):
        if self._cornerOutOfBounds(corners[0][0], corners[0][1]) or \
            self._cornerOutOfBounds(corners[1][0], corners[1][1]) or \
            self._cornerOutOfBounds(corners[2][0], corners[2][1]) or \
                self._cornerOutOfBounds(corners[3][0], corners[3][1]):
            return True

        return False

    def square_is_cut(self, corners):
        # check if any corner is outside of the image and that at least one corner is inside
        if self.square_out_of_bounds(corners) is False:
            return False

        corners_outside = 0
        if corners[0][0] < 0 or corners[0][0] > self.image_width or corners[0][1] < 0 or corners[0][1] > self.image_height:
            corners_outside += 1
        if corners[1][0] < 0 or corners[1][0] > self.image_width or corners[1][1] < 0 or corners[1][1] > self.image_height:
            corners_outside += 1
        if corners[2][0] < 0 or corners[2][0] > self.image_width or corners[2][1] < 0 or corners[2][1] > self.image_height:
            corners_outside += 1
        if corners[3][0] < 0 or corners[3][0] > self.image_width or corners[3][1] < 0 or corners[3][1] > self.image_height:
            corners_outside += 1

        if corners_outside >= 3:
            return False

        return True

    def circle_out_of_bounds(self, x, y, radius):
        if x - radius < 0 or x + radius > self.image_width or \
                    y - radius < 0 or y + radius > self.image_height:
            return True

        return False

    def make_circle(self, x=None, y=None, radius=None, color=None, dist_idx=None, background_color=None):
        isOutOfBounds = True
        if color is None:
            color = self._generate_nonmatching_color(background_color)

        if radius is None and dist_idx is not None:
            radius = np.sqrt(self.circle_areas_distribution[dist_idx] / np.pi)

        if dist_idx is None and radius is None:
            radius = np.random.choice(self.circle_areas_distribution)
            radius = np.sqrt(radius / np.pi)

        if x is None:
            x = np.random.uniform(0, self.image_width - radius)

        if y is None:
            y = np.random.uniform(0, self.image_height - radius)

        if radius is None:
            radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)

        isOutOfBounds = self.circle_out_of_bounds(x, y, radius)
        max_tries = 5
        tries = 0
        while isOutOfBounds is True:
            if tries >= max_tries:
                radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)
                tries = 0
            x = np.random.uniform(0, self.image_width - radius)
            y = np.random.uniform(0, self.image_height - radius)

            isOutOfBounds = self.circle_out_of_bounds(x, y, radius)
            tries += 1

        circle = Circle((x, y), radius, color=color)
        circle.set_antialiased(True)
        shape = geometry.Point(x, y).buffer(radius)

        return circle, shape, radius

    def _generate_nonmatching_color(self, *excluded_colors):
        while True:
            color = np.random.rand(3)
            if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
                return color

    def _cornerOutOfBounds(self, x, y):
        if x < 0:
            return True
        if x > self.image_width:
            return True

        if y < 0:
            return True
        if y > self.image_height:
            return True

        return False

    def save_graphs(self, folder=""):
        if self.square_collection.contains_data():
            self.square_collection.save_area_histogram(folder=folder)
            self.square_collection.save_distance_histogram(folder=folder)
            self.square_collection.save_area_linegraph(folder=folder)

        if self.circle_collection.contains_data():
            self.circle_collection.save_area_histogram(folder=folder)
            self.circle_collection.save_distance_histogram(folder=folder)
            self.circle_collection.save_area_linegraph(folder=folder)

        swc_folder = folder + "/SWC"
        if os.path.isdir(swc_folder) is False:
            os.mkdir(swc_folder)
        if self.swc_collection.contains_data():
            self.swc_collection.save_area_histogram(folder=swc_folder, variant="both")
            self.swc_collection.save_area_histogram(folder=swc_folder, variant=None) # Does 2 hist (test & train)
            # self.swc_collection.save_area_linegraph(folder=swc_folder)

    def save_metadata(self, folder=""):
        if self.square_collection.size_train > 0 or self.square_collection.size_test > 0:
            self.square_collection.write_to_csv(folder=folder)

        if self.circle_collection.size_train > 0 or self.circle_collection.size_test > 0:
            self.circle_collection.write_to_csv(folder=folder)

        if self.swc_collection.size_train > 0 or self.swc_collection.size_test > 0:
            self.swc_collection.write_to_csv(folder=folder)
