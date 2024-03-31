from Generator import Generator
import os
from time import perf_counter as pc

DATASET_DIRECTORY_NAME = "Datasets/Dataset_A3"
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


def delete_empty_dirs(dir):
    for filename in os.listdir(dir):
        if os.path.isdir(dir + filename):
            if len(os.listdir(dir + filename)) == 0:
                os.rmdir(dir + filename)


# Delete old test dataset
del_dir(TRAIN_DIRECTORY)
del_dir(TEST_DIRECTORY)

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

test_quantity = 100
train_quantity = 300 / 3

print("Starting to generate images")
generator = Generator(seed=406)
start = pc()


# generator.generate_images(False, True, True, SQUARE_CIRCLE_TRAIN_DIRECTORY, train_quantity, variant="train")
# generator.generate_images(False, True, False, CIRCLE_TRAIN_DIRECTORY, train_quantity, variant="train")
generator.generate_images(False, False, True, True, SQUARE_TRAIN_DIRECTORY, train_quantity, variant="train")

# generator.generate_images(False, True, True, SQUARE_CIRCLE_TEST_DIRECTORY, test_quantity, variant="test")
# generator.generate_images(False, True, False, TEST_DIRECTORY, test_quantity, variant="test")
generator.generate_images(False, False, True, True, TEST_DIRECTORY, test_quantity, variant="test")


end = pc()
time = round(end - start, 4)
print("\nFinished generating images (" + str(time) + "s)")
start_2 = pc()

# move images from test to subdirectory
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

delete_empty_dirs(TEST_DIRECTORY)
delete_empty_dirs(TRAIN_DIRECTORY)

end = pc()
time = round(end - start_2, 4)
print("Finished moving images (" + str(time) + "s)")
start_2 = pc()

# Save seed to file
with open(DATASET_DIRECTORY_NAME + "/seed.txt", "w") as f:
    f.write(str(generator.seed))

end = pc()
time = round(end - start_2, 4)
print("Finished writing seed file (" + str(time) + "s)")
start_2 = pc()

generator.save_graphs(folder=DATASET_GRAPH_DIRECTORY)
generator.save_metadata(folder=DATASET_DATA_DIRECTORY)

end = pc()
time = round(end - start_2, 4)
print("Finished generating graphs (" + str(time) + "s)")
time = round(end - start, 4)
print("Finished generation (" + str(time) + "s)")
