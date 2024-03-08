from PIL import Image, ImageDraw
import random

MARGIN = 5
def AddRectangle(draw, width, height, x, y, color):
    draw.rectangle([x, y, x + width, y + height], fill=color)

def AddSquare(draw, size, x, y, color):
    draw.rectangle([x, y, x + size, y + size], fill=color)
def AddCircle(draw, radius, x, y, color):
    draw.ellipse([x, y, x + radius, y + radius], fill=color)
def GenerateRGBColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
def CheckIntersect(square_x, square_y, square_width, square_height, circle_x, circle_y, circle_radius):
    closest_x = max(square_x, min(circle_x, square_x + square_width))
    closest_y = max(square_y, min(circle_y, square_y + square_height))

    # Calculate the distance between the circle's center and the closest point
    distance = ((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2) ** 0.5

    # Check if the distance is less than or equal to the circle's radius
    # If true, there is an intersection; return True. Otherwise, return False.
    return distance <= circle_radius
def Generate(num_images, img_size, folder):
    if (num_images <= 0) or (img_size <= 0):
        raise ValueError('Invalid Parameters for Generation')

    for i in range(num_images):
        img = Image.new('RGB', (img_size, img_size), GenerateRGBColor())
        draw = ImageDraw.Draw(img)
        square_size = random.randint(0, img_size - 1)
        square_x = random.randint(0, img_size - square_size + MARGIN)
        square_y = random.randint(0, img_size - square_size + MARGIN)
        color = GenerateRGBColor()
        AddSquare(draw, square_size, square_x, square_y, color)
        color = GenerateRGBColor()
        circle_radius = random.randint(0, img_size - MARGIN)
        circle_x = random.randint(0, img_size - circle_radius + MARGIN)
        circle_y = random.randint(0, img_size - circle_radius - MARGIN)
        while CheckIntersect(square_x, square_y, square_size, square_size, circle_x, circle_y, circle_radius) != True:
            circle_x = random.randint(0, img_size - circle_radius + MARGIN)
            circle_y = random.randint(0, img_size - circle_radius - MARGIN)
            circle_radius = random.randint(0, img_size - MARGIN)
        AddCircle(draw, circle_radius, circle_x, circle_y, color)
        img.save(folder + "/square" + str(i) + ".jpg")


Generate(20, 500, "Dataset/test")