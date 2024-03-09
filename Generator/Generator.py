import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class Generator:
    def __init__(self, image_width=500, image_height=500, seed=None):
        self.num_images = 0
        self.image_width = image_width
        self.image_height = image_height
        self.seed = seed
        self.min_square_side_length = 8
        self.min_circle_radius = 4

        self.max_circle_radius = image_width / 4
        self.max_square_side_length = image_width / 2
        if seed == None:
            rand_seed = np.random.randint(0, 1000)
            np.random.seed(rand_seed)
            self.seed = rand_seed
            print(f"Seed not provided. Using random seed {rand_seed}")
        else:
            np.random.seed(seed)

    def generate_images(self, draw_random=False, draw_circle=False, draw_square=False, directory="dataset", quantity=1):
        np.random.seed(self.seed)
        i = 0
        while i < quantity:
            if draw_random:
                draw_circle = np.random.choice([True, False])
                draw_square = np.random.choice([True, False])
            background_color = self._generate_nonmatching_color()
            fig = plt.figure(figsize=(self.image_width / 100, self.image_height / 100), facecolor=background_color)
            ax = fig.add_subplot(111)
                          
            if draw_square:
                filename = "square_"
                square_color = self._generate_nonmatching_color(background_color)
                side_length = np.random.uniform(self.min_square_side_length, self.max_square_side_length)
                square_x = np.random.uniform(0, self.image_width - side_length)
                square_y = np.random.uniform(0, self.image_height - side_length)

                # Check for overlap with the circle 
                """
                if draw_circle:
                    while self._circleIntersectsSquare(square_x, square_y, side_length, circle_x, circle_y, radius) == True:
                        side_length = np.random.uniform(self.min_square_side_length, self.max_square_side_length)
                        square_x = np.random.uniform(0, self.image_width - side_length)
                        square_y = np.random.uniform(0, self.image_height - side_length)
                """

                        
                        
                square = Rectangle((square_x, square_y), side_length, side_length, color=square_color)
                ax.add_patch(square)

            if draw_circle:
                if draw_square:
                    filename += "circle_"
                else:
                    filename = "circle_"
                circle_color = self._generate_nonmatching_color(background_color)
                radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)
                circle_x = np.random.uniform(0, self.image_width - radius)
                circle_y = np.random.uniform(0, self.image_height - radius)

                # Check for overlap with the square
                """
                if draw_square:
                    while (square_x - radius < circle_x < square_x + side_length + radius) and \
                            (square_y - radius < circle_y < square_y + side_length + radius):
                        radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)
                        circle_x = np.random.uniform(0, self.image_width - radius)
                        circle_y = np.random.uniform(0, self.image_height - radius)
                """

                if draw_square:
                    while self._circleIntersectsSquare(square_x, square_y, side_length, circle_x, circle_y, radius) == True:
                        radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)
                        circle_x = np.random.uniform(0, self.image_width - radius)
                        circle_y = np.random.uniform(0, self.image_height - radius)

                # Check if circle is outside image bounds
                if circle_x - radius < 0 or circle_x + radius > self.image_width or \
                    circle_y - radius < 0 or circle_y + radius > self.image_height:
                    plt.close()
                    continue

                circle = Circle((circle_x, circle_y), radius, color=circle_color)
                ax.add_patch(circle)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')
            if draw_square == False and draw_circle == False:
                filename = "none_"
            plt.savefig(f'{directory + "/" + filename + str(i+1)}.jpg', bbox_inches='tight', pad_inches=0)
            plt.close()
            self.num_images += 1
            i += 1

    def _generate_nonmatching_color(self, *excluded_colors):
        while True:
            color = np.random.rand(3)
            if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
                return color
            
    def _circleIntersectsSquare(self, sq_x, sq_y, sq_side, c_x, c_y, radius):
        distX = abs(c_x - sq_x - sq_side / 2)
        distY = abs(c_y - sq_y - sq_side / 2)

        if (distX > (sq_side / 2 + radius)):
            return False
        if (distY > (sq_side / 2 + radius)):
            return False
        
        if (distX <= (sq_side / 2)):
            return True
        if (distY <= (sq_side / 2)):
            return True
        
        cornerDist_sq = (distX - sq_side / 2) ** 2 + (distY - sq_side / 2) ** 2

        return (cornerDist_sq <= (radius ** 2))