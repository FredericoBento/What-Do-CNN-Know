from Generator import Generator
import os
from time import perf_counter as pc

TEST_DIRECTORY = "dataset/test"
SQUARE_TEST_DIRECTORY = "dataset/test/square"
CIRCLE_TEST_DIRECTORY = "dataset/test/circle"
SQUARE_CIRCLE_TEST_DIRECTORY = "dataset/test/square_circle"

def del_dir(rootdir):
    if(os.path.isdir(rootdir)):
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames: os.remove(rootdir+'/'+filename)
            for dirname in dirnames: del_dir(rootdir+'/'+dirname)
        os.rmdir(rootdir)


# Delete old test dataset
del_dir(TEST_DIRECTORY)

os.makedirs(TEST_DIRECTORY, exist_ok=True)
os.makedirs(SQUARE_TEST_DIRECTORY, exist_ok=True)
os.makedirs(CIRCLE_TEST_DIRECTORY, exist_ok=True)
os.makedirs(SQUARE_CIRCLE_TEST_DIRECTORY, exist_ok=True)

print("Starting to generate images")
generator = Generator()
start = pc()
generator.generate_images(False, True, SQUARE_TEST_DIRECTORY, "square", 20)
generator.generate_images(True, False, CIRCLE_TEST_DIRECTORY, "circle", 20)
generator.generate_images(True, True, SQUARE_CIRCLE_TEST_DIRECTORY, "square_circle", 500)

# Save seed to file
with open("dataset/test/seed.txt", "w") as f:
    f.write(str(generator.seed))

end = pc()
print("Finished generating images in " + str(end - start ) + " seconds")
