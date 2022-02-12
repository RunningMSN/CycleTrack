from itertools import cycle
import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(cycle_data,title):
    loc_df = converters.convert_map(cycle_data,aggregate=False)
    fig = go.Figure(
        data = go.Scattergeo(
            lon=loc_df["Long"],
            lat = loc_df["Lat"],
            text = loc_df["School"]+"<br>Best Outcome: "+loc_df["Best Outcome"].str.replace("_"," ").str.title(),
            hoverinfo="text",
            marker = dict(size = 10),
            marker_color=loc_df["color"]
        )
    )
    fig.update_layout(
        title=title,
        geo_scope = 'usa',
        height = 500,
        margin = dict(l=25,r=25,t=25,b=25)
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
