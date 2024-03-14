from Generator import Generator
import os
from time import perf_counter as pc

DATASET_DIRECTORY_NAME = "dataset"
DATASET_GRAPH_DIRECTORY = DATASET_DIRECTORY_NAME + "/graphs"

TRAIN_DIRECTORY = DATASET_DIRECTORY_NAME + "/train/"
TEST_DIRECTORY = DATASET_DIRECTORY_NAME + "/test/"

CIRCLE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "circle"
NONE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "none"
SQUARE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "square"
SQUARE_CIRCLE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "square_circle"


CIRCLE_TEST_DIRECTORY = TEST_DIRECTORY + "circle"

NONE_TEST_DIRECTORY = TEST_DIRECTORY + "none"
SQUARE_TEST_DIRECTORY = TEST_DIRECTORY + "square"
SQUARE_CIRCLE_TEST_DIRECTORY = TEST_DIRECTORY + "square_circle"

folders = [CIRCLE_TRAIN_DIRECTORY, NONE_TRAIN_DIRECTORY,
           SQUARE_TRAIN_DIRECTORY, SQUARE_CIRCLE_TRAIN_DIRECTORY,
           CIRCLE_TEST_DIRECTORY, NONE_TEST_DIRECTORY,
           SQUARE_TEST_DIRECTORY, SQUARE_CIRCLE_TEST_DIRECTORY,
           DATASET_GRAPH_DIRECTORY]


def del_dir(rootdir):
    if os.path.isdir(rootdir):
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames:
                os.remove(rootdir+'/'+filename)
            for dirname in dirnames:
                del_dir(rootdir+'/'+dirname)
        os.rmdir(rootdir)


# Delete old test dataset
del_dir(TRAIN_DIRECTORY)
del_dir(TEST_DIRECTORY)

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)


test_quantity = 1000
train_quantity = 3000 / 2

print("Starting to generate images")
generator = Generator()
start = pc()

# generator.generate_images(draw_random=True, directory=TEST_DIRECTORY, quantity=test_quantity)
#
# generator.generate_images(False, False, True, SQUARE_TRAIN_DIRECTORY, train_quantity)
# generator.generate_images(False, True, False, CIRCLE_TRAIN_DIRECTORY, train_quantity)
# generator.generate_images(False, False, False, NONE_TRAIN_DIRECTORY, train_quantity)
# generator.generate_images(False, True, True, SQUARE_CIRCLE_TRAIN_DIRECTORY, train_quantity)

generator.generate_images(False, False, True, SQUARE_TRAIN_DIRECTORY, train_quantity)
generator.generate_images(False, False, False, NONE_TRAIN_DIRECTORY, train_quantity)

generator.generate_images(False, False, True, TEST_DIRECTORY, test_quantity)
generator.generate_images(False, False, False, TEST_DIRECTORY, test_quantity)



# move image from test to subdirectory
for filename in os.listdir(TEST_DIRECTORY):
    if os.path.isdir(TEST_DIRECTORY + filename):
        continue
    if filename.__contains__("square_circle_"):
        os.rename(TEST_DIRECTORY + filename, SQUARE_CIRCLE_TEST_DIRECTORY + "/" + filename)
    elif filename.__contains__("circle_"):
        os.rename(TEST_DIRECTORY + filename, CIRCLE_TEST_DIRECTORY + "/" + filename)
    elif filename.__contains__("square_"):
        os.rename(TEST_DIRECTORY + filename, SQUARE_TEST_DIRECTORY + "/" + filename)
    else:
        os.rename(TEST_DIRECTORY + filename, NONE_TEST_DIRECTORY + "/" + filename)

# Save seed to file
with open(DATASET_DIRECTORY_NAME + "/seed.txt", "w") as f:
    f.write(str(generator.seed))

end = pc()
print("Finished generating images in " + str(end - start) + " seconds")

generator.getAreaHistogram(folder=DATASET_GRAPH_DIRECTORY)
generator.getAreaLineGraph(folder=DATASET_GRAPH_DIRECTORY)
