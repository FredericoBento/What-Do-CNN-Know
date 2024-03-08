import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class Generator:
    def __init__(self, image_width=500, image_height=500, seed=None):
        self.num_images = 0
        self.image_width = image_width
        self.image_height = image_height
        self.seed = seed
        self.min_square_side_length = 5
        self.min_circle_radius = 2
        if seed == None:
            rand_seed = np.random.randint(0, 1000)
            np.random.seed(rand_seed)
            self.seed = rand_seed
            print(f"Seed not provided. Using random seed {rand_seed}")
        else:
            np.random.seed(seed)

    def generate_images(self, draw_circle=True, draw_square=False, directory="dataset", filename="shapes", quantity=1):
        np.random.seed(self.seed)
        i = 0
        while i < quantity:
            background_color = self._generate_nonmatching_color()
            fig = plt.figure(figsize=(self.image_width / 100, self.image_height / 100), facecolor=background_color)
            ax = fig.add_subplot(111)
            if draw_square:
                square_color = self._generate_nonmatching_color(background_color)
                side_length = np.random.uniform(1, min(self.image_width, self.image_height)) // 4
                square_x = np.random.uniform(0, self.image_width - side_length)
                square_y = np.random.uniform(0, self.image_height - side_length)

                square = Rectangle((square_x, square_y), side_length, side_length, color=square_color)
                ax.add_patch(square)

                image_width_adjusted = self.image_width - side_length
                image_height_adjusted = self.image_height - side_length
            else:
                image_width_adjusted = self.image_width
                image_height_adjusted = self.image_height

            if draw_circle:
                circle_color = self._generate_nonmatching_color(background_color)
                max_radius = min(image_width_adjusted, image_height_adjusted)
                radius = np.random.uniform(1, max_radius)
                circle_x = np.random.uniform(0, image_width_adjusted - radius)
                circle_y = np.random.uniform(0, image_height_adjusted - radius)

                # Check for overlap with the square
                if draw_square:
                    while (square_x - radius < circle_x < square_x + side_length + radius) and \
                            (square_y - radius < circle_y < square_y + side_length + radius):
                        radius = np.random.uniform(10, max_radius)
                        circle_x = np.random.uniform(0, image_width_adjusted - radius)
                        circle_y = np.random.uniform(0, image_height_adjusted - radius)

                # Check if circle is outside image bounds
                if circle_x - radius < 0 or circle_x + radius > image_width_adjusted or \
                    circle_y - radius < 0 or circle_y + radius > image_height_adjusted:
                    plt.close()
                    continue

                circle = Circle((circle_x, circle_y), radius, color=circle_color)
                ax.add_patch(circle)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')

            plt.savefig(f'{directory + "/" + filename + str(i+1)}.jpg', bbox_inches='tight', pad_inches=0)
            plt.close()
            self.num_images += 1
            i += 1

    def _generate_nonmatching_color(self, *excluded_colors):
        while True:
            color = np.random.rand(3)
            if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
                return color