import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from shapely import geometry
from scipy.interpolate import interp1d
from numpy import asarray
from numpy import savetxt
import sys
# increase pyplot speed
plt.rcParams['agg.path.chunksize'] = 10000



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

        self.squares_area = []
        self.circle_area = []

        self.circle_radius = []
        self.lenghts = []

        self.square_areas_distribution = []
        self.circle_areas_distribution = []

        if seed is None:
            rand_seed = np.random.randint(0, 1000)
            np.random.seed(rand_seed)
            self.seed = rand_seed
            print(f"Seed not provided. Using random seed {rand_seed}")
        else:
            print(f"Seed provided. Using seed {seed}")
            np.random.seed(seed)

    def generate_images(self, draw_random=False, draw_circle=False, draw_square=False, directory="dataset", quantity=1):

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

        while i < quantity:
            b = f"Generating image {i+1}/{quantity}"
            sys.stdout.write('\r'+b)
            if draw_random:
                draw_circle = np.random.choice([True, False])
                draw_square = np.random.choice([True, False])
            background_color = self._generate_nonmatching_color()

            fig = plt.figure(figsize=(figure_width, figure_height), facecolor=background_color, linewidth=0.0)
            ax = fig.add_subplot(111)
            ax.set_rasterized(True)
            radius = -1
            length = -1
            if draw_square:
                filename = "square_"
                square, shape_square, length = self.makeSquare(background_color=background_color, dist_idx=i)

            if draw_circle:
                if draw_square:
                    filename += "circle_"
                else:
                    filename = "circle_"
                circle, shape_circle, radius = self.makeCircle(background_color=background_color, dist_idx=i)

                if draw_square:
                    if shape_square.intersects(shape_circle):
                        while shape_square.intersects(shape_circle):
                            circle, shape_circle, radius = self.makeCircle(background_color=background_color, dist_idx=None)
                            square, shape_square, length = self.makeSquare(background_color=background_color, dist_idx=None)
                
                ax.add_patch(circle)
                area = (radius**2) * np.pi
                self.circle_area.append(area)
                self.circle_radius.append(radius)

            if draw_square and length > 0:
                ax.add_patch(square)
                self.squares_area.append(length * length)
                self.lenghts.append(length)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')

            if draw_square is False and draw_circle is False:
                filename = "none_"
        
            plt.savefig(f'{directory + "/" + filename + str(i+1)}.png', bbox_inches='tight', pad_inches=0, dpi=106.5)
            plt.close()

            self.num_images += 1
            i += 1
        return self.num_images, self.squares_area, self.circle_area

    def makeSquare(self, x=None, y=None, angle=None, length=None, color=None, background_color=None, dist_idx=None):
        isOutoffBounds = True
        
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

        isOutoffBounds = self.square_out_of_bounds(corners)

        while isOutoffBounds is True:
        
            x = np.random.uniform(0, self.image_width - length)
            y = np.random.uniform(0, self.image_height - length)

            angle = np.random.uniform(0, 360)

            center_x = x + length / 2
            center_y = y + length / 2
            square = Rectangle((x, y), length, length, color=color, angle=angle, rotation_point=(center_x, center_y))
            corners = square.get_corners()

            isOutoffBounds = self.square_out_of_bounds(corners)

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
    
    def circle_out_of_bounds(self, x, y, radius):
        if x - radius < 0 or x + radius > self.image_width or \
                    y - radius < 0 or y + radius > self.image_height:
            return True
        
        return False
        
    def makeCircle(self, x=None, y=None, radius=None, color=None, dist_idx=None, background_color=None):
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

        while isOutOfBounds is True:
            x = np.random.uniform(0, self.image_width - radius)
            y = np.random.uniform(0, self.image_height - radius)
            
            isOutOfBounds = self.circle_out_of_bounds(x, y, radius)
        
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

    def getRadiusHistogram(self, circle_radius=None, folder=None, title=""):
        if circle_radius is None:
            circle_radius = self.circle_radius

        if len(circle_radius) > 0:
            max = np.max(circle_radius)
            min = np.min(circle_radius)
            interval = 10
            hist = plt.hist(circle_radius, bins=np.arange(min, max+1, interval), color="red")
            plt.xlabel("Radius")
            plt.ylabel("Number of Samples")
            plt.title(title)
            plt.grid(True)
            fig = plt.gcf()
            fig.set_size_inches(10, 5)
            filename = 'Radius_Histogram_seed_' + str(self.seed) + '.png'
            if folder is not None:
                filename = folder + "/" + filename
            fig.savefig(filename, dpi=100)
            plt.close()
        else:
            print("No Data has been generated yet, failed to generate graph")

    def getSquareLengthHistogram(self, lengths=None, folder=None, title=""):
        if lengths is None:
            lengths = self.lenghts
        
        if len(lengths) > 0:
            max = np.max(lengths)
            min = np.min(lengths)
            interval = 10
            hist = plt.hist(lengths, bins=np.arange(min, max+1, interval), color="blue")
            plt.xlabel("Length")
            plt.ylabel("Number of Samples")
            plt.title(title)
            plt.grid(True)
            fig = plt.gcf()
            fig.set_size_inches(10, 5)
            filename = 'Length_Histogram_seed_' + str(self.seed) + '.png'
            if folder is not None:
                filename = folder + "/" + filename
            fig.savefig(filename, dpi=100)
            plt.close()


    def getAreaHistogram(self, circle_areas=None, square_areas=None, folder=None, title=""):
        if circle_areas is None:
            circle_areas = self.circle_area

        if square_areas is None:
            square_areas = self.squares_area

        data = []
        colors = []
        labels = ["Circles"]
        text = ""
        if len(circle_areas) > 0 and len(square_areas) > 0:
            data = [square_areas, circle_areas]
            colors = ["blue", "red"]
            labels = ["Circles", "Squares"]
            text = "Total Circles: " + str(len(circle_areas)) + " Total Squares: " + str(len(square_areas))
        elif len(circle_areas) > 0:
            data = [circle_areas]
            colors = ["red"]
            text = "Total Circles: " + str(len(circle_areas))
        elif len(square_areas) > 0:
            data = [square_areas]
            colors = ["blue"]
            labels = ["Squares"]
            text = "Total Squares: " + str(len(square_areas))
        else:
            print("No Data has been generated yet, failed to generate graph")
            return
        
        if len(data) > 2:
            c_max = np.max(data[1])
            c_min = np.min(data[1])

            s_max = np.max(data[0])
            s_min = np.min(data[0])

            max = c_max if c_max > s_max else s_max
            min = c_min if c_min < s_min else s_min

        else:
            max = np.max(data[0])
            min = np.min(data[0])

        interval = 2000
        hist = plt.hist(data, bins=np.arange(min, max+1, interval), color=colors,label=labels)

        plt.text(0.5, 0.95, text, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.xlabel("Areas")
        plt.ylabel("Number of Samples")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        filename = 'Dataset_Histogram_seed_' + str(self.seed) + '.png'
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def getAreaLineGraph(self, circle_areas=None, square_areas=None, folder=None, title=""):
        if circle_areas is None:
            circle_areas = self.circle_area

        if square_areas is None:
            square_areas = self.squares_area

        square_areas = np.sort(square_areas)
        circle_areas = np.sort(circle_areas)

        square_len = len(square_areas)
        circle_len = len(circle_areas)

        if square_len < 0 and circle_len < 0:
            print("No Data has been generated yet, failed to generate graph")
            return

        if square_len > 0 and circle_len <= 0:
            return self.squareLineGraph(squareAreas=square_areas, folder=folder)
        elif circle_len > 0 and square_len <= 0:
            return self.circleLineGraph(circleAreas=circle_areas, folder=folder)

        if square_len > 0 and circle_len > 0:

            x1 = np.linspace(0, 1, len(square_areas))
            x2 = np.linspace(0, 1, len(circle_areas))

            # Interpolate data2 to match the length of data1
            f = interp1d(x2, circle_areas)
            data2_interp = f(x1)

            plt.plot(x1, square_areas, color='blue', label='Square Areas (' + str(len(square_areas)) + ')')
            plt.plot(x2, data2_interp, color='red', label='Circle Areas' + str(len(circle_areas)) + ')')

            plt.xlabel('Number of Samples')
            plt.ylabel('Areas')
            plt.title(title)
            plt.legend()
            plt.grid(True)
            fig = plt.gcf()
            fig.set_size_inches(10, 5)
            filename = 'Dataset_Line_seed_' + str(self.seed) + '.png'
            if folder is not None:
                filename = folder + "/" + filename
            fig.savefig(filename, dpi=100)
            plt.close()

    def squareLineGraph(self, squareAreas=None, folder=None):
        if squareAreas is None:
            squareAreas = self.squares_area

        squareAreas = np.sort(squareAreas)
        square_len = len(squareAreas)
        if square_len > 0:
            x1 = np.linspace(0, 1, len(squareAreas))

        # Plot the line graph
        if square_len > 0:
            plt.plot(x1, squareAreas, color='blue', label='Square Areas (' + str(len(squareAreas)) + ')')

        plt.xlabel('Number of Samples')
        plt.ylabel('Areas')
        plt.title('Comparison of Areas')
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        filename = 'Dataset_Line_seed_' + str(self.seed) + '.png'
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def circleLineGraph(self, circleAreas=None, folder=None):
        if circleAreas is None:
            circleAreas = self.circle_area

        circleAreas = np.sort(circleAreas)
        circle_len = len(circleAreas)
        if circle_len > 0:
            x1 = np.linspace(0, 1, len(circleAreas))

        # Plot the line graph
        if circle_len > 0:
            plt.plot(x1, circleAreas, color='red', label='Circle Areas (' + str(len(circleAreas)) + ')')

        plt.xlabel('Number of Samples')
        plt.ylabel('Areas')
        plt.title('Circle Areas')
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        filename = 'Dataset_Line_seed_' + str(self.seed) + '.png'
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def saveMetadata(self, folder=""):
        square_data = asarray(self.squares_area)
        circle_data = asarray(self.circle_area)
        filename = folder + "/square_data.csv"
        savetxt(filename, square_data, delimiter=",")

        filename = folder + "/circle_data.csv"
        savetxt(filename, circle_data, delimiter=",")
    



