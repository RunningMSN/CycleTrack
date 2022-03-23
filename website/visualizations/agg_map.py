import plotly
import plotly.graph_objects as go
import json
import numpy as np
from . import converters

def scaler(dfseries,max_num,min_num):
    new_series = []
    for i in dfseries:
        new_val = ((i - dfseries.min()) / (dfseries.max() - dfseries.min())) * (max_num - min_num) + min_num
        new_series.append(new_val)
    return new_series


def generate(data):
    df = converters.convert_map(data,aggregate=True)
    loc_df = df.groupby(["School","Long","Lat"]).size().reset_index()
    loc_df = loc_df.rename(columns={0:"Count"})
    
    urls = ["/explorer/"+i for i in loc_df.School]

    fig = go.Figure()
    data = go.Scattergeo(
            lon=loc_df["Long"],
            lat = loc_df["Lat"],
            text = loc_df["School"] + "<br>Applications: " + (loc_df["Count"]).astype(str),
            hoverinfo="text",
            marker = dict(size = (scaler(loc_df["Count"],20,3))),
            customdata = urls,
        )
    fig.add_trace(data)
    fig.update_layout(
        geo_scope = 'north america',
        height = 700,
        margin = dict(l=25,r=25,t=25,b=25),
        clickmode="event"
    )
    fig.update_geos(resolution=50,fitbounds="locations")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
