import ShapesGenerator
import random

generator = ShapesGenerator.ShapesGenerator()

color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

generator.GenerateCanvasWithSquare(10, 500, 500, color)
generator.SaveCanvas("Dataset/test", "square")