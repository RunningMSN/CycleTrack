from itertools import cycle
import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(data,title):
    df = converters.convert_map(data)
    loc_df = df.groupby(["School","Long","Lat"]).size().reset_index()
    loc_df = loc_df.rename(columns={0:"Count"})
    #raise ValueError(loc_df)
    fig = go.Figure()
    data = go.Scattergeo(
            lon=loc_df["Long"],
            lat = loc_df["Lat"],
            text = loc_df["School"] + ": "+ (loc_df["Count"]).astype(str),
            hoverinfo="text",
            marker = dict(size = loc_df["Count"]*10)
        )
    fig.add_trace(data)
    fig.update_layout(
        title=title,
        geo_scope = 'usa',
        height = 800
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
