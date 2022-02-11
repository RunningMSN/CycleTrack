from itertools import cycle
import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(cycle_data,title):
    loc_df = converters.convert_map(cycle_data)
    fig = go.Figure(
        data = go.Scattergeo(
            lon=loc_df["Long"],
            lat = loc_df["Lat"],
            text = loc_df["School"],
            hoverinfo="text",
            marker = dict(size = 10)
        )
    )
    fig.update_layout(
        title=title,
        geo_scope = 'usa',
        height = 800
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
