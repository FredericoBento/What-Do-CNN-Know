import numpy as np
import matplotlib.pyplot as plt
import csv


class Circle:
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.area = 3.14159 * radius * radius


class CircleCollection:
    def __init__(self, seed, train=False):
        self.size = 0
        self.circles = []
        self.areas = []
        self.train = train
        self.tag = "(TEST)"
        self.filename_tag = "Test"
        self.seed = seed
        if self.train:
            self.tag = "(TRAIN)"
            self.filename_tag = "Train"

    def add_circle(self, radius, x, y):
        if radius < 0:
            print("Radius cannot be negative")
            return
        circle = Circle(radius, x, y)
        self.circles.append(circle)
        self.area.append(circle.area)
        self.size += 1

    def save_area_linegraph(self, filename, folder=None):
        if self.size < 2:
            print("Not enough samples to generate linegraph")
            return

        if filename is None:
            filename = "Circle_Areas_Linegraph_"

        filename = filename + self.filename_tag + "_" + str(self.seed) + ".png"

        circleAreas = np.sort(self.areas)

        x1 = np.linspace(0, 1, self.size)
        plt.plot(x1, circleAreas, color='blue', label='Circle Areas (' + str(self.size) + ')')

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
            print("No circles to write to file")
            return

        if filename is None:
            filename = "Circles_" + self.filename_tag + "_" + str(self.seed) + ".csv"

        if folder is not None:
            filename = folder + "/" + filename

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Radius', 'Area', 'X', 'Y'])
            for circle in self.circles:
                writer.writerow([circle.radius, circle.area, circle.x, circle.y])
