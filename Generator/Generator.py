import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class Generator:
    def __init__(self, image_width=500, image_height=500, seed=None):
        self.num_images = 0
        self.image_width = image_width
        self.image_height = image_height
        self.seed = seed
        if seed:
            np.random.seed(seed)

    def generate_images(self, draw_circle=True, draw_square=False, directory="dataset", filename="shapes", quantity=1):
        for i in range(quantity):
            # filename = "none_"
            background_color = self._generate_nonmatching_color()
            fig = plt.figure(figsize=(self.image_width / 100, self.image_height / 100), facecolor=background_color)
            ax = fig.add_subplot(111)
            if draw_square:
                # filename += "square_"
                square_color = self._generate_nonmatching_color(background_color)
                side_length = np.random.randint(1, min(self.image_width, self.image_height)) // 4
                square_x = np.random.randint(0, self.image_width - side_length)
                square_y = np.random.randint(0, self.image_height - side_length)

                square = Rectangle((square_x, square_y), side_length, side_length, color=square_color)
                ax.add_patch(square)

                image_width_adjusted = self.image_width - side_length
                image_height_adjusted = self.image_height - side_length
            else:
                image_width_adjusted = self.image_width
                image_height_adjusted = self.image_height

            if draw_circle:
                # filename += "circle_"
                circle_color = self._generate_nonmatching_color(background_color)
                max_radius = min(image_width_adjusted, image_height_adjusted) // 4
                radius = np.random.randint(10, max_radius)
                circle_x = np.random.randint(radius, image_width_adjusted - radius)
                circle_y = np.random.randint(radius, image_height_adjusted - radius)

                # Check for overlap with the square
                if draw_square:
                    while (square_x - radius < circle_x < square_x + side_length + radius) and \
                            (square_y - radius < circle_y < square_y + side_length + radius):
                        circle_x = np.random.randint(radius, image_width_adjusted - radius)
                        circle_y = np.random.randint(radius, image_height_adjusted - radius)

                circle = Circle((circle_x, circle_y), radius, color=circle_color)
                ax.add_patch(circle)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')

            plt.savefig(f'{directory + "/" + filename + str(i+1)}.jpg', bbox_inches='tight', pad_inches=0)
            plt.close()
            self.num_images += 1

    def _generate_nonmatching_color(self, *excluded_colors):
        while True:
            color = np.random.rand(3)
            if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
                return color