import numpy as np
import matplotlib.pyplot as plt
import csv


class Square:
    def __init__(self, length, angle, x, y, distance=None, img_width=500, img_height=500):
        self.length = length
        self.area = length * length
        self.x = x
        self.y = y
        self.angle = angle
        self.center_x = x + length / 2
        self.center_y = y + length / 2
        if distance is None:
            self.distance_from_center = np.sqrt((self.center_x - img_width / 2) ** 2 + (self.center_y - img_height / 2) ** 2)
        else:
            self.distance_from_center = distance


class SquareCollection:
    def __init__(self, seed, img_width=500, img_height=500):
        self.squares_train = []
        self.squares_test = []

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

    def load_from_csv(self, filename=None, variant=None):
        if variant is None:
            print("Variant not specified, (test or train)")
            return
        elif variant != "train" and variant != "test":
            print("Invalid variant")
            return

        if filename is None:
            print("Filename not specified")
            return
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 5:
                    length = int(row[0])
                    angle = int(row[1])
                    x = int(row[2])
                    y = int(row[3])
                    if len(row) == 6:
                        distance = int(row[4])
                        self.add_square(length, angle, x, y, distance, variant=variant)
                    else:
                        self.add_square(length, angle, x, y, variant=variant)
                else:
                    print("Invalid row")
                    return

    def add_square(self, length, angle, x, y, img_width=500, img_height=500, distance_from_center=None, variant=None):
        if img_width < 0 or img_height < 0:
            print("Image dimensions cannot be negative")
            return

        if variant is None:
            print("Variant not specified, (test or train)")
            return
        if variant == "train":
            self.add_square_train(length, angle, x, y, distance_from_center)
        elif variant == "test":
            self.add_square_test(length, angle, x, y, distance_from_center)
        else:
            print("Invalid variant")
            return

    def add_square_train(self, length, angle, x, y, distance_from_center=None):
        if length < 0:
            print("Length cannot be negative")
            return
        if x < 0 or y < 0:
            print("Coordinates cannot be negative")
            return
        square = Square(length, angle, x, y, distance_from_center, self.img_width, self.img_height)
        self.squares_train.append(square)
        self.areas_train.append(square.area)
        self.size_train += 1

    def add_square_test(self, length, angle, x, y, distance_from_center=None):
        if length < 0:
            print("Length cannot be negative")
            return
        square = Square(length, angle, x, y, distance_from_center, self.img_width, self.img_height)
        self.squares_test.append(square)
        self.areas_test.append(square.area)
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
            filename = "Square_Areas_Histogram_"

        filename = filename + filename_tag + "_" + str(self.seed) + ".png"

        colors = ["red"]
        labels = ["Squares"]
        text = "Squares (" + str(size) + ")"
        title = "Square Areas " + tag

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
        squares = None
        if variant is None:
            self.save_distance_histogram(None, folder, "train")
            self.save_distance_histogram(None, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            squares = self.squares_train
            filename_tag = self.filename_tag_train
            tag = self.tag_train
        elif variant == "test":
            size = self.size_test
            squares = self.squares_test
            filename_tag = self.filename_tag_test
            tag = self.tag_test
        else:
            print("Invalid variant")
            return
        if size < 1:
            print("Not enough samples to generate histogram")
            return
        if filename is None:
            filename = "Square_Distance_Histogram_"
        filename = filename + filename_tag + "_" + str(self.seed) + ".png"
        colors = ["red"]
        labels = ["Squares"]
        text = "Squares (" + str(size) + ")"
        title = "Square Distance from Center " + tag
        max = np.max([square.distance_from_center for square in squares])
        min = np.min([square.distance_from_center for square in squares])
        interval = 50
        hist = plt.hist([square.distance_from_center for square in squares], bins=np.arange(min, max+1, interval), color=colors, label=labels)
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
            filename = "Square_Areas_Linegraph_"

        filename = filename + filename_tag + "_" + str(self.seed) + ".png"
        squareAreas = np.sort(areas)

        x1 = np.linspace(0, 1, size)
        plt.plot(x1, squareAreas, color='red', label='Square Areas (' + str(size) + ')')

        plt.xlabel('Number of Samples')
        plt.ylabel('Areas')
        plt.title('Square Areas Linegraph ' + tag)
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
        squares = None

        if variant is None:
            self.write_to_csv(filename, folder, "train")
            self.write_to_csv(filename, folder, "test")
            return
        if variant == "train":
            size = self.size_train
            squares = self.squares_train
            filename_tag = self.filename_tag_train
            size = self.size_train
        elif variant == "test":
            self.size_test
            squares = self.squares_test
            filename_tag = self.filename_tag_test
            size = self.size_test
        else:
            print("Invalid variant")
            return

        if size < 1:
            print("No squares to write to file")
            return

        if filename is None:
            filename = "Squares_" + filename_tag + "_" + str(self.seed) + ".csv"

        if folder is not None:
            filename = folder + "/" + filename

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Length', 'Area', 'X', 'Y', 'Angle', 'Distance_From_Center'])
            for square in squares:
                writer.writerow([square.length, square.area, square.x, square.y, square.angle, square.distance_from_center])
