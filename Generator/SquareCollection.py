import numpy as np
import matplotlib.pyplot as plt
import csv


class Square:
    def __init__(self, length, angle, x, y):
        self.length = length
        self.area = length * length
        self.x = x
        self.y = y
        self.angle = angle


class SquareCollection:
    def __init__(self, seed, train=False):
        self.size = 0
        self.squares = []
        self.areas = []
        self.train = train
        self.tag = "(TEST)"
        self.filename_tag = "Test"
        self.seed = seed
        if self.train:
            self.tag = "(TRAIN)"
            self.filename_tag = "Train"

    def add_square(self, length, angle, x, y):
        if length < 0:
            print("Length cannot be negative")
            return
        square = Square(length, angle, x, y)
        self.square.append(square)
        self.areas.append(square.area)
        self.size += 1

    def get_max_area(self):
        max = np.max(self.areas)
        return max

    def get_min_area(self):
        min = np.min(self.areas)
        return min

    def save_area_histogram(self, filename=None, folder=None):
        if self.size < 1:
            print("Not enough samples to generate histogram")
            return

        if filename is None:
            filename = "Square_Areas_Histogram" 

        filename = filename + self.filename_tag + "_" + str(self.seed) + ".png"

        colors = ["red"]
        labels = ["Squares"]
        text = "Squares (" + str(self.size) + ")"
        title = "Square Areas " + self.tag

        max = self.get_max_area()
        min = self.get_min_area()

        interval = 2000
        hist = plt.hist(self.areas, bins=np.arange(min, max+1, interval), color=colors, label=labels)

        plt.text(0.5, 0.95, text, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.xlabel("Areas")
        plt.ylabel("Number of Samples")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)

        filename = filename + str(self.seed) + '.png'

        if folder is not None:
            filename = folder + "/" + filename

        fig.savefig(filename, dpi=100)
        plt.close()

    def save_area_linegraph(self, filename=None, folder=None):
        if self.size < 2:
            print("Not enough samples to generate linegraph")
            return

        if filename is None:
            filename = "Square_Areas_Linegraph_"

        filename = filename + self.filename_tag + "_" + str(self.seed) + ".png"
        squareAreas = np.sort(self.areas)

        x1 = np.linspace(0, 1, self.size)
        plt.plot(x1, squareAreas, color='red', label='Square Areas (' + str(self.size) + ')')

        plt.xlabel('Number of Samples')
        plt.ylabel('Areas')
        plt.title('Comparison of Areas')
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def write_to_csv(self, filename=None, folder=None):
        if self.size < 1:
            print("No squares to write to file")
            return

        if filename is None:
            filename = "Squares_" + self.filename_tag + "_" + str(self.seed) + ".csv"

        if folder is not None:
            filename = folder + "/" + filename

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Length', 'Area', 'X', 'Y', 'Angle'])
            for square in self.squares:
                writer.writerow([square.length, square.area, square.x, square.y, square.angle])
