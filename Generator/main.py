from Generator import Generator
import os

TEST_DIRECTORY = "dataset/test"
SQUARE_TEST_DIRECTORY = "dataset/test/square"
CIRCLE_TEST_DIRECTORY = "dataset/test/circle"
SQUARE_CIRCLE_TEST_DIRECTORY = "dataset/test/square_circle"

os.makedirs(TEST_DIRECTORY, exist_ok=True)
os.makedirs(SQUARE_TEST_DIRECTORY, exist_ok=True)
os.makedirs(CIRCLE_TEST_DIRECTORY, exist_ok=True)
os.makedirs(SQUARE_CIRCLE_TEST_DIRECTORY, exist_ok=True)

generator = Generator()
generator.generate_images(False, True, SQUARE_TEST_DIRECTORY, "square", 20)
generator.generate_images(True, False, CIRCLE_TEST_DIRECTORY, "circle", 20)
generator.generate_images(True, True, SQUARE_CIRCLE_TEST_DIRECTORY, "square_circle", 20)

# Save seed to file
with open("dataset/test/seed.txt", "w") as f:
    f.write(str(generator.seed))