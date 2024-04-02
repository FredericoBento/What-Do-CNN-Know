import PlotMaker as pm

plot_maker = pm.PlotMaker()

GRAPH_FOLDER = "graphs/"

circles_test = "../Generator/Datasets/Dataset_C2/data/Circles_Test_676.csv"
circles_train = "../Generator/Datasets/Dataset_C2/data/Circles_Train_676.csv"

filename = "Circles_Test_676_Area_Histogram"

data_filename = circles_test
output_filename = "Circles_Test_676_Area_Histogram"
folder = GRAPH_FOLDER
title = "Area Histogram of Circles_676 (TEST)"
color = "Blue"
shape = "Circle"

plot_maker.area_histogram(
    data_filename=data_filename,
    output_filename=output_filename,
    folder=folder,
    title=title,
    color=color,
    shape=shape
)

output_filename = "Circles_Test_676_Distance_Histogram"
title = "Distance From Center Circles_676 (TRAIN)"
color = "Red"

plot_maker.distance_from_center_histogram(
    data_filename=circles_test,
    output_filename=output_filename,
    folder=folder,
    title=title,
    color=color,
    shape=shape
)

