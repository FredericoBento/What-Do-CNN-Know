from CircleCollection import CircleCollection
from SquareCollection import SquareCollection
import numpy as np
import csv
import matplotlib.pyplot as plt


class SquareWithCircleCollection:
    def __init__(self, seed):
        self.circle_collection = CircleCollection(seed)
        self.square_collection = SquareCollection(seed)

        self.tag_train = "(TRAIN)"
        self.tag_test = "(TEST)"

        self.filename_tag_train = "Train"
        self.filename_tag_test = "Test"

        self.size_train = 0
        self.size_test = 0

        self.seed = seed

    def load_from_csv(self, filename=None, variant=None):
        if variant is None:
            print("Variant not specified, (test or train)")
            return
        elif variant != "train" and variant != "test":
            print("Invalid variant")
            return

        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 'Length':
                    continue
                if row[0] == 'Radius':
                    continue
                if len(row) == 5:
                    self.add_square(float(row[0]), float(row[1]), float(row[2]), float(row[3]), variant)
                elif len(row) == 6:
                    self.add_circle(float(row[0]), float(row[2]), float(row[3]), variant)
            if variant == "train":
                if len(self.square_collection.areas_train) != len(self.circle_collection.areas_train):
                    print("Number of squares and circles do not match")
                self.size_train = len(self.square_collection.areas_train)
            elif variant == "test":
                if len(self.square_collection.areas_test) != len(self.circle_collection.areas_test):
                    print("Number of squares and circles do not match")
                self.size_test = len(self.square_collection.areas_test)


    def contains_data(self, variant=None, form=None):
        if variant is None:
            if form is None:
                retval = self.contains_data("train")
                if retval is False:
                    retval = self.contains_data("test")
            elif form == "circle":
                retval = self.circle_collection.contains_data(variant)
            elif form == "square":
                retval = self.square_collection.contains_data(variant)
            return retval

        if variant == "train":
            if form is None:
                if self.size_train < 1:
                    return False
                else:
                    return True
            elif form == "circle":
                return self.circle_collection.contains_data(variant)
            elif form == "square":
                return self.square_collection.contains_data(variant)

        elif variant == "test":
            if form is None:
                if self.size_test < 1:
                    return False
                else:
                    return True
            elif form == "circle":
                return self.circle_collection.contains_data(variant)
            elif form == "square":
                return self.square_collection.contains_data(variant)
        else:
            print("Invalid variant")
            return

    def add_square(self, length, angle, x, y, variant=None):
        if variant is None:
            print("Variant not specified, (test or train)")
            return
        elif variant == "train":
            self.add_square_train(length, angle, x, y)
        elif variant == "test":
            self.add_square_test(length, angle, x, y)

    def add_square_train(self, length, angle, x, y):
        self.square_collection.add_square_train(length, angle, x, y)
        # self.size_train += 1

    def add_square_test(self, length, angle, x, y):
        self.square_collection.add_square_test(length, angle, x, y)
        # self.size_test += 1

    def add_circle(self, radius, x, y, variant=None):
        if variant is None:
            print("Variant not specified, (test or train)")
            return
        elif variant == "train":
            self.add_circle_train(radius, x, y)
        elif variant == "test":
            self.add_circle_test(radius, x, y)

    def add_circle_train(self, radius, x, y):
        self.circle_collection.add_circle_train(radius, x, y)

    def add_circle_test(self, radius, x, y):
        self.circle_collection.add_circle_test(radius, x, y)

    def get_max_area(self, areas):
        max = np.max(areas)
        return max

    def get_min_area(self, areas):
        min = np.min(areas)
        return min

    def increase_size(self, variant):
        if variant == "train":
            self.size_train += 1
        elif variant == "test":
            self.size_test += 1

    def save_area_histogram(self, filename=None, folder=None, form=None, variant=None):
        size = 0
        filename_tag = None
        tag = None
        areas = None

        if form is None:
            colors = ["red", "blue"]
            labels = ["Squares", "Circles"]
            title = "Squares with Circles Areas"
            text = "Squares with Circles"
            if filename is None:
                filename = "SWC_Areas_Histogram_"
        elif form == "circle":
            colors = ["blue"]
            labels = ["Circles"]
            title = "Circles Areas"
            text = "Circles"
            if filename is None:
                filename = "(SWC) Circles_Areas_Histogram_"
        elif form == "square":
            colors = ["red"]
            labels = ["Squares"]
            title = "Squares Areas"
            text = "Squares"
            if filename is None:
                filename = "(SWC) Squares_Areas_Histogram_"
        else:
            print("Invalid form")
            return

        if variant is None:
            self.save_area_histogram(None, folder, form, "train")
            self.save_area_histogram(None, folder, form, "test")
            return
        if variant == "train":
            size = self.size_train
            if form is None:
                areas = [self.square_collection.areas_train, self.circle_collection.areas_train]
            elif form == "circle":
                areas = self.circle_collection.areas_train
            elif form == "square":
                areas = self.square_collection.areas_train

            filename_tag = self.filename_tag_train
            tag = self.tag_train

        elif variant == "test":
            size = self.size_test
            if form is None:
                areas = [self.square_collection.areas_test, self.circle_collection.areas_test]
            elif form == "circle":
                areas = self.circle_collection.areas_test
            elif form == "square":
                areas = self.square_collection.areas_test

            filename_tag = self.filename_tag_test
            tag = self.tag_test

        elif variant == "both":
            size = self.size_train + self.size_test
            filename_tag = "Train_Test"
            tag = "(TRAIN + TEST)"
            if form is None:
                sq_copy = self.square_collection.areas_train.copy()
                sq_copy.extend(self.square_collection.areas_test)
                cir_copy = self.circle_collection.areas_train.copy()
                cir_copy.extend(self.circle_collection.areas_test)
                areas = [sq_copy, cir_copy]
            elif form == "circle":
                areas = self.circle_collection.areas_train
                areas.extend(self.circle_collection.areas_test)
            elif form == "square":
                areas = self.square_collection.areas_train
                areas.extend(self.square_collection.areas_test)

        if size < 1:
            print("Not enough samples to generate histogram")
            return

        filename = filename + filename_tag + "_" + str(self.seed) + ".png"
        title = title + " " + tag
        text = text + " (" + str(size) + ")"

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
            squares = self.square_collection.squares_train
            circles = self.circle_collection.circles_train
            filename_tag = self.filename_tag_train
            size = self.size_train
        elif variant == "test":
            self.size_test
            squares = self.square_collection.squares_test
            circles = self.circle_collection.circles_test
            filename_tag = self.filename_tag_test
            size = self.size_test
        else:
            print("Invalid variant")
            return

        if size < 1:
            print("No circles to write to file")
            return

        if filename is None:
            filename = "SWC_" + filename_tag + "_" + str(self.seed) + ".csv"

        if folder is not None:
            filename = folder + "/" + filename

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['Length', 'Area', 'X', 'Y', 'Angle', 'Distance_From_Center'])
            for square in squares:
                writer.writerow([square.length, square.area, square.x, square.y, square.angle, square.distance_from_center])
            writer.writerow(['Radius', 'Area', 'X', 'Y', 'Distance_From_Center'])
            for circle in circles:
                writer.writerow([circle.radius, circle.area, circle.x, circle.y, square.distance_from_center])
