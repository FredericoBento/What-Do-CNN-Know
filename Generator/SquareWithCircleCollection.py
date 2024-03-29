from CircleCollection import CircleCollection
from SquareCollection import SquareCollection
import numpy as np


class SquareWithCircleCollection:
    def __init__(self, square_collection=None, circle_collection=None, seed, train=False):
        if circle_collection_collection is None:
            self.circles = CircleCollection(seed, train)
        else:
            self.circles = circle_collection

        if square_collection is None:
            self.squares = SquareCollection(seed, train)
        else:
            self.squares = square_collection

        self.seed = seed
        self.train = train
        self.tag = "(TEST)"
        self.filename_tag = "Test"
        if self.train:
            self.tag = "(TRAIN)"
            self.filename_tag = "Train"

    def save_area_histogram(self, filename=None, folder=None):
        data_len = 0
        data = []
        colors = ["red, blue"]
        labels = ["Squares", "Circles"]
        text = "Squares and Circles"

        if filename is None:
            filename = "Square_Circle_Areas_Histogram_"

        if self.squares.size > 0:
            data.append(self.squares.areas)
            data_len += 1

        if self.circles.size > 0:
            data.append(self.circles.areas)
            data_len += 1

        if data is None:
            print("Could not generate histogram. No data provided")
            return
        else:
            data_len = len(data)

        if data_len > 2:
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

        filename = filename + str(self.seed) + '.png'

        if folder is not None:
            filename = folder + "/" + filename
        fig.savefig(filename, dpi=100)
        plt.close()
