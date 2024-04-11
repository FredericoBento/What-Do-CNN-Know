# takes an csv and groups the failed images in a folder
import os
import shutil

image_folder = '../Generator/Datasets/Dataset_E/test/'
output_folder = '../CNN_Model/Test_5/results/5-1/failed_images/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

folder = "../CNN_Model/Test_5/results/5-1/"
counter = 0

with open(folder + 'failed_filenames.txt', 'r') as f:
    for line in f:
        line = line.split('/')
        line = line[-2:]
        line[1] = line[1].strip()
        output_file = output_folder + line[0] + '/' + line[1]
        image = image_folder + line[0] + '/' + line[1]
        
        shutil.copy(image, output_file)
        counter += 1
        print("Copied", image, "to", output_file)

    
folder = "../CNN_Model/Test_5/results/5-1/results.csv"

circles_csv = "../Generator/Datasets/Dataset_E2/data/Circles_Test_744.csv"
Squares_csv = "../Generator/Datasets/Dataset_E2/data/Squares_Test_744.csv"
swc = "../Generator/Datasets/Dataset_E2/data/SWC_Test_744.csv"

c_csv = open(circles_csv, 'r')
sq_csv = open(Squares_csv, 'r')
swc_csv = open(swc, 'r')

swc_failed = open(output_folder + 'swc_failed.csv', 'w')
c_failed = open(output_folder + 'c_failed.csv', 'w')
sq_failed = open(output_folder + 'sq_failed.csv', 'w')

folder = "../CNN_Model/Test_5/results/5-1/failed_images/"

circles = []
swc_circles = []
squares = []

for filename in os.listdir(folder + "circle"):
    if os.path.isdir(filename):
        continue
    if filename.__contains__("square"):
        swc_circles.append(filename)
    else:
        circles.append(filename)

for filename in os.listdir(folder + "no_circle"):
    if os.path.isdir(filename):
        continue
    squares.append(filename)


print("Circles:", len(circles))
# copy data from c_csv to c_failed
with open(circles_csv, 'r') as f:
    for line in f:
        if line.split(',')[0] in circles:
            c_failed.write(line)

print("Squares:", len(squares))
# copy data from sq_csv to sq_failed
with open(Squares_csv, 'r') as f:
    for line in f:
        if line.split(',')[0] in squares:
            sq_failed.write(line)

print("SWC:", len(swc_circles))
# copy data from swc_csv to swc_failed
with open(swc, 'r') as f:
    for line in f:
        if line.split(',')[0] in swc_circles:
            swc_failed.write(line)

c_csv.close()
sq_csv.close()
swc_csv.close()

c_failed.close()
sq_failed.close()
swc_failed.close()
 
            

        
        
    
        
