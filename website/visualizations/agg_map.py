import plotly
import plotly.graph_objects as go
import json
import numpy as np
from . import converters

def scaler(dfseries,r):
    min = dfseries.min()
    max = dfseries.max()
    range = max - min
    new_series = (((dfseries - min)/range)*(r-1)+1)*6
    return new_series


def generate(data):
    df = converters.convert_map(data,aggregate=True)
    loc_df = df.groupby(["School","Long","Lat"]).size().reset_index()
    loc_df = loc_df.rename(columns={0:"Count"})
    
    max_num = loc_df["Count"].max()
    min_num = loc_df["Count"].min()

    max_size = 30
    min_size = 1

    marker_scale = (max_size - min_size)/(max_num - min_num) + min_size

    fig = go.Figure()
    data = go.Scattergeo(
            lon=loc_df["Long"],
            lat = loc_df["Lat"],
            text = loc_df["School"] + "<br>Applications: " + (loc_df["Count"]).astype(str),
            hoverinfo="text",
            marker = dict(size = (scaler(loc_df["Count"],marker_scale)))
        )
    fig.add_trace(data)
    fig.update_layout(
        geo_scope = 'usa',
        height = 500,
        margin = dict(l=25,r=25,t=25,b=25)
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
