from Generator import Generator
import os
from time import perf_counter as pc

DATASET_DIRECTORY_NAME = "Datasets/Dataset_A2"
DATASET_GRAPH_DIRECTORY = DATASET_DIRECTORY_NAME + "/graphs"
DATASET_DATA_DIRECTORY = DATASET_DIRECTORY_NAME + "/data"

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
           DATASET_GRAPH_DIRECTORY, DATASET_DATA_DIRECTORY]


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

test_quantity = 100
train_quantity = 300 / 2

print("Starting to generate images")
generator = Generator(seed=406)
start = pc()


generator.generate_images(False, True, False, CIRCLE_TRAIN_DIRECTORY, train_quantity, train=True)
generator.generate_images(False, False, False, NONE_TRAIN_DIRECTORY, train_quantity, train=True)

generator.generate_images(False, True, False, TEST_DIRECTORY, test_quantity)
generator.generate_images(False, False, False, TEST_DIRECTORY, test_quantity)


end = pc()
print("\nFinished generating images in " + str(end - start) + " seconds")
start_2 = pc()

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

end = pc()
print("\nFinished moving images in " + str(end - start_2) + " seconds")
start_2 = pc()

# Save seed to file
with open(DATASET_DIRECTORY_NAME + "/seed.txt", "w") as f:
    f.write(str(generator.seed))

end = pc()
print("\nFinished writing seed file" + str(end - start_2) + " seconds")
start_2 = pc()

# generator.g_area_histogram(folder=DATASET_GRAPH_DIRECTORY, title="Square and Circle Areas")
# generator.g_area_line_graph(folder=DATASET_GRAPH_DIRECTORY, title="Square and Circle Areas")
#
# generator.g_radius_histogram(folder=DATASET_GRAPH_DIRECTORY, title="Circle Radius")
# generator.g_square_length_histogram(folder=DATASET_GRAPH_DIRECTORY, title="Square Length")

generator.save_graphs(folder=DATASET_GRAPH_DIRECTORY)
generator.save_metadata(folder=DATASET_DATA_DIRECTORY)

end = pc()
print("\nFinished generating graphs" + str(end - start_2) + " seconds")
print("\nFinished generation" + str(end - start) + " seconds")
