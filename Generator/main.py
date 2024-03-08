from Generator import Generator
import os
from time import perf_counter as pc

TRAIN_DIRECTORY = "dataset/train/"
TEST_DIRECTORY = "dataset/test/"

SQUARE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "square"
CIRCLE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "circle"
SQUARE_CIRCLE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "square_circle"
NONE_TRAIN_DIRECTORY = TRAIN_DIRECTORY + "none"

SQUARE_AND_CIRCLE_TEST_DIRECTORY = TEST_DIRECTORY + "square_and_circle"



def del_dir(rootdir):
    if(os.path.isdir(rootdir)):
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames: os.remove(rootdir+'/'+filename)
            for dirname in dirnames: del_dir(rootdir+'/'+dirname)
        os.rmdir(rootdir)


# Delete old test dataset
del_dir(TRAIN_DIRECTORY)
del_dir(TEST_DIRECTORY)

# Create new directories
os.makedirs(TRAIN_DIRECTORY, exist_ok=True)
os.makedirs(TEST_DIRECTORY, exist_ok=True)

os.makedirs(SQUARE_TRAIN_DIRECTORY, exist_ok=True)
os.makedirs(CIRCLE_TRAIN_DIRECTORY, exist_ok=True)
os.makedirs(NONE_TRAIN_DIRECTORY, exist_ok=True)
os.makedirs(SQUARE_CIRCLE_TRAIN_DIRECTORY, exist_ok=True)

os.makedirs(SQUARE_AND_CIRCLE_TEST_DIRECTORY, exist_ok=True)


test_quantity = 1000
train_quantity = 3000 / 4

print("Starting to generate images")
generator = Generator()
start = pc()
generator.generate_images(False, False, True, SQUARE_TRAIN_DIRECTORY, train_quantity)
generator.generate_images(False, True, False, CIRCLE_TRAIN_DIRECTORY, train_quantity)
generator.generate_images(False, False, False, NONE_TRAIN_DIRECTORY, train_quantity)
generator.generate_images(False, True, True, SQUARE_CIRCLE_TRAIN_DIRECTORY, train_quantity)

generator.generate_images(draw_random=True, directory=SQUARE_AND_CIRCLE_TEST_DIRECTORY, quantity=test_quantity)



# Save seed to file
with open("dataset/seed.txt", "w") as f:
    f.write(str(generator.seed))

end = pc()
print("Finished generating images in " + str(end - start ) + " seconds")
