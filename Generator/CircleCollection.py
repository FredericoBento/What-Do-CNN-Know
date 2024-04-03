import numpy as np
import matplotlib.pyplot as plt
import csv


class Circle:
    def __init__(self, radius, x, y, distance=None, filename=None, img_width=500, img_height=500):
        self.filename = filename
        self.radius = radius
        self.x = x
        self.y = y
        self.area = 3.14159 * radius * radius
        if distance is None:
            self.distance_from_center = np.sqrt((x - img_width/2)**2 + (y - img_height/2)**2)
        else:
            self.distance_from_center = distance


class CircleCollection:
    def __init__(self, seed, img_width=500, img_height=500):
        self.circles_train = []
        self.circles_test = []

        self.areas_train = []
        self.areas_test = []

        self.tag_train = "(TRAIN)"
        self.tag_test = "(TEST)"

        self.filename_tag_train = "Train"
        self.filename_tag_test = "Test"

        self.size_train = 0
        self.size_test = 0

        self.seed = seed
        self.img_width = img_width
        self.img_height = img_height

    def contains_data(self, variant=None):
        if variant is None:
            retval = self.contains_data("train")
            if retval is False:
                retval = self.contains_data("test")
            return retval
        if variant == "train":
            if self.size_train < 1:
                return False
            else:
                return True
        elif variant == "test":
            if self.size_test < 1:
                return False
            else:
                return True
        else:
            print("Invalid variant")
            return

    def add_circle(self, radius, x, y, distance_from_center=None, variant=None):
        if variant is None:
            print("Variant not specified, (test or train)")
            return
        if variant == "train":
            self.add_circle_train(radius, x, y, distance_from_center)
        elif variant == "test":
            self.add_circle_test(radius, x, y, distance_from_center)
        else:
            print("Invalid variant")
            return

    def add_circle_train(self, radius, x, y, distance_from_center=None):
        if radius < 0:
            print("radius cannot be negative")
            return
        filename = "circle_" + str(self.size_train+1) + ".png"
        circle = Circle(radius, x, y, distance_from_center, filename, img_width=self.img_width, img_height=self.img_height)
        self.circles_train.append(circle)
        self.areas_train.append(circle.area)
        self.size_train += 1

    def add_circle_test(self, radius, x, y, distance_from_center=None):
        if radius < 0:
            print("radius cannot be negative")
            return
        filename = "circle_" + str(self.size_test+1) + ".png"
        circle = Circle(radius, x, y, distance_from_center, filename, img_width=self.img_width, img_height=self.img_height)
        self.circles_test.append(circle)
        self.areas_test.append(circle.area)
        self.size_test += 1

    def get_max_area(self, areas):
        max = np.max(areas)
        return max

    def get_min_area(self, areas):
        min = np.min(areas)
        return min

    def save_area_histogram(self, filename=None, folder=None, variant=None):
        size = 0
        filename_tag = None
        tag = None
        areas = None

        if variant is None:
            self.save_area_histogram(None, folder, "train")
            self.save_area_histogram(None, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            areas = self.areas_train
            filename_tag = self.filename_tag_train
            tag = self.tag_train
        elif variant == "test":
            size = self.size_test
            areas = self.areas_test
            filename_tag = self.filename_tag_test
            tag = self.tag_test
        else:
            print("Invalid variant")
            return

        if size < 1:
            print("Not enough samples to generate histogram")
            return

        if filename is None:
            filename = "Circle_Areas_Histogram_"

        filename = filename + filename_tag + "_" + str(self.seed) + ".png"

        colors = ["blue"]
        labels = ["Circles"]
        text = "Circles (" + str(size) + ")"
        title = "Circle Areas " + tag

        max = self.get_max_area(areas)
        min = self.get_min_area(areas)

        interval = 2000
        hist = plt.hist(areas, bins=np.arange(min, max+1, interval), color=colors, label=labels)

        plt.text(0.5, 0.95, text, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.xlabel("Areas")
        plt.ylabel("Number of Samples")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)

        if folder is not None:
            filename = folder + "/" + filename

        fig.savefig(filename, dpi=100)
        plt.close()

    def save_distance_histogram(self, filename=None, folder=None, variant=None):
        size = 0
        filename_tag = None
        tag = None
        circles = None
        if variant is None:
            self.save_distance_histogram(filename, folder, "train")
            self.save_distance_histogram(filename, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            circles = self.circles_train
            filename_tag = self.filename_tag_train
            tag = self.tag_train
        elif variant == "test":
            size = self.size_test
            circles = self.circles_test
            filename_tag = self.filename_tag_test
            tag = self.tag_test
        else:
            print("Invalid variant")
            return
        if size < 1:
            print("Not enough samples to generate histogram")
            return
        if filename is None:
            filename = "Circle_Distance_Histogram_"
        filename = filename + filename_tag + "_" + str(self.seed) + ".png"
        colors = ["blue"]
        labels = ["Circles"]
        text = "Circles (" + str(size) + ")"
        title = "Circle Distance from Center " + tag
        max = np.max([circle.distance_from_center for circle in circles])
        min = np.min([circle.distance_from_center for circle in circles])
        interval = 10
        hist = plt.hist([circle.distance_from_center for circle in circles], bins=np.arange(min, max+1, interval), color=colors, label=labels)
        plt.text(0.5, 0.95, text, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.xlabel("Distance from Center")
        plt.ylabel("Number of Samples")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def save_area_linegraph(self, filename=None, folder=None, variant=None):
        filename_tag = None
        tag = None
        areas = None
        size = 0

        if variant is None:
            self.save_area_linegraph(filename, folder, "train")
            self.save_area_linegraph(filename, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            areas = self.areas_train
            filename_tag = self.filename_tag_train
            tag = self.tag_train
        elif variant == "test":
            size = self.size_test
            areas = self.areas_test
            filename_tag = self.filename_tag_test
            tag = self.tag_test

        if size < 2:
            print("Not enough samples to generate linegraph")
            return

        if filename is None:
            filename = "Circle_Areas_Linegraph_"

        filename = filename + filename_tag + "_" + str(self.seed) + ".png"
        circleAreas = np.sort(areas)

        x1 = np.linspace(0, 1, size)
        plt.plot(x1, circleAreas, color='blue', label='Circle Areas (' + str(size) + ')')

        plt.xlabel('Number of Samples')
        plt.ylabel('Areas')
        plt.title('Circle Areas Linegraph ' + tag)
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()

    def write_to_csv(self, filename=None, folder=None, variant=None):
        size = 0
        filename_tag = None
        circles = None

        if variant is None:
            self.write_to_csv(filename, folder, "train")
            self.write_to_csv(filename, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            circles = self.circles_train
            filename_tag = self.filename_tag_train
            size = self.size_train
        elif variant == "test":
            self.size_test
            circles = self.circles_test
            filename_tag = self.filename_tag_test
            size = self.size_test
        else:
            print("Invalid variant")
            return

        if size < 1:
            print("No circles to write to file")
            return

        if filename is None:
            filename = "Circles_" + filename_tag + "_" + str(self.seed) + ".csv"

        if folder is not None:
            filename = folder + "/" + filename

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Filename', 'Radius', 'Area', 'X', 'Y', 'Distance_From_Center'])
            for circle in circles:
                writer.writerow([circle.filename, circle.radius, circle.area, circle.x, circle.y, circle.distance_from_center])
