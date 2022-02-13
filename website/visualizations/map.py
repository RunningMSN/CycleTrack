import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(cycle_data,title):
    loc_df = converters.convert_map(cycle_data,aggregate=False)
    fig = go.Figure()

    outcomes = list(loc_df["Best Outcome"].unique())
    for outcome in outcomes:
        outcome_df = loc_df.loc[loc_df["Best Outcome"] == outcome]
        fig.add_trace(go.Scattergeo(
            lon=outcome_df["Long"],
            lat = outcome_df["Lat"],
            text = outcome_df["School"]+"<br>Best Outcome: "+converters.action_names[outcome],
            hoverinfo="text",
            marker = dict(size = 10),
            marker_color=outcome_df["color"],
            name = converters.action_names[outcome]
        ))

    fig.update_layout(
        title=title,
        #title_x = 0.5,
        geo_scope = 'usa', width = 850,height = 400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    fig.add_layout_image(
        dict(
        source="./static/images/CycleTrack-Watermark3.png",
        xref="x domain",
        yref="y domain",
        x=1, y=1,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom")
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
