import Canvas
import Square
import Circle
import random
class ShapesGenerator:
    def __init__(self):
        self.canvas = []
        self.num_canvas = 0

    def GenerateCanvasWithSquare(self, num, width, height, color):
        for i in range(num):
            canvas = Canvas.Canvas(width, height, tuple(color))
            max = width
            if width < height:
                max = height
            canvas.DrawSquare(self.RandomSquare(0, width, max))
            self.canvas.append(canvas)
            self.num_canvas += 1


    def GenerateCanvasWithCircle(self, num, width, height, color):
        pass

    def GenerateCanvasWithSquareAndCircle(self, num, width, height, color):
        pass

    def SaveCanvas(self, directory, filename):
        i = 1
        for canvas in self.canvas:
            canvas.Save(directory, filename + str(i))
            i += 1

    def RandomSquare(self, max_x, max_y, max_size):
        random.Random()
        x = random.uniform(0.00, max_x)
        y =  random.uniform(0, max_y)
        size = random.uniform(0.00, max_size)
        color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        return Square.Square(x, y, size, color)

