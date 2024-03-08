from PIL import Image, ImageDraw
import Square
import Circle
class Canvas(object):
    def __init__(self, width, height, color):
        self.img = Image.new('RGB', (width, height), color)
        self.drawing = ImageDraw.Draw(self.img)
        self.width = width
        self.height = height
        self.color = color
        self.num_squares = 0
        self.num_circles = 0

    def Draw(self):
        self.drawing = ImageDraw.Draw(self.img)

    def DrawSquare(self, s):
        self.drawing.rectangle([s.x, s.y, s.x + s.size, s.y + s.size], fill=s.color)
        self.num_squares += 1

    def DrawCircle(self, c):
        self.drawing.ellipse([c.x, c.y, c.x + c.radius, c.y + c.radius], fill=c.color)
        self.num_circles += 1

    def Save(self, directory, filename):
        self.img.save(directory + "/" + filename + ".jpg")


