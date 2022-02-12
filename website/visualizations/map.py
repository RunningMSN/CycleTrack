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
        title_x = 0.5,
        geo_scope = 'usa', width = 800,height =500,
        margin = dict(l = 0, r = 0,b = 0, t = 30,pad = 0),
        images=[dict(
        source="./static/images/Docs2Be.png",
        xref="paper", yref="paper",
        x=0, y=0,
        sizex=0.08, sizey=0.08,
        xanchor="left", yanchor="bottom"
      )]
    )

    fig.add_annotation(
        text="Created with CycleTrack",
        xref="paper", yref="paper",
        x=0.5, y=1.03, 
        showarrow=False)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
