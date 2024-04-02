import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

class PlotMaker:
    def __init__(self):
        pass

    def read_data(self, data_filename):
        if data_filename.endswith('.csv'):
            return pd.read_csv(data_filename)

    def area_histogram(self, data_filename, output_filename, folder="graphs", title="", color="Blue", shape=""):
        data = self.read_data(data_filename)
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data['Area'],
            marker_color=color,
            marker_line_color='black',
            marker_line_width=0.5,
            opacity=0.75,
            xbins=dict(
                start=0,
                end=60_000,
                size=5_000
            )
        ))
        fig.update_xaxes(
            tick0=0,
            dtick=5_000
        )
        fig.update_layout(title=title)
        shape_title = shape + "s"
        fig.update_yaxes(title_text='Number of ' + shape_title)

        self.write_html(fig, folder, output_filename)
        self.write_image(fig, folder, output_filename)
        return fig
    
    def distance_from_center_histogram(self, data_filename, output_filename, folder="graphs", title="", color="Blue", shape=""):
        data = self.read_data(data_filename)
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data['Distance_From_Center'],
            marker_color=color,
            marker_line_color='black',
            marker_line_width=0.5,
            opacity=0.75,
            xbins = dict( 
                start=0,
                end=500,
                size=50
            )
        ))
        fig.update_xaxes(
            tick0=0,
            dtick=50
        )
        fig.update_layout(title=title)
        fig.update_yaxes(title_text='Number of ' + shape + "s")

        self.write_html(fig, folder, output_filename)
        self.write_image(fig, folder, output_filename)
        return fig
    
    def write_image(self, fig, folder, filename):
        if os.path.exists(folder) == False:
            os.mkdir(folder)
        if os.path.exists(folder + "/png") == False:
            os.mkdir(folder + "/png")
        
        folder = folder + "/png/"
        file = open(folder + filename + ".png", "wb")
        fig.write_image(file)
        file.close()
        return fig
    
    def write_html(self, fig, folder, filename):
        if os.path.exists(folder) == False:
            os.mkdir(folder)
        if os.path.exists(folder + "/html") == False:
            os.mkdir(folder + "/html")
        
        folder = folder + "/html/"    
        file = open(folder + filename + ".html", "w")
        fig.write_html(file)
        file.close()
        return fig  
 
    