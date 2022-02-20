import plotly
import plotly.graph_objects as go
import json
from ..models import Cycle, School
from . import converters


def cycle_progress(name, year, phd):
    schools = School.query.filter_by(name=name, phd=phd).all()
    dates = {"Secondary Received" : [], "Interview Received" : [], "Acceptance Received" : []}
    # Filter schools by criteria
    for school in schools:
        cycle = Cycle.query.filter_by(id=school.cycle_id).first()
        if cycle.cycle_year == year:
            if school.secondary_received:
                dates["Secondary Received"].append(school.secondary_received)
            if school.interview_received:
                dates["Interview Received"].append(school.interview_received)
            if school.acceptance:
                dates["Acceptance Received"].append(school.acceptance)

    # No data to display
    if len(dates["Secondary Received"]) == 0 and len(dates["Interview Received"]) == 0 and len(dates["Acceptance Received"]) == 0:
        return None

    # Build traces
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=dates["Secondary Received"],
                               name='Secondary Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["secondary_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=dates["Interview Received"],
                               name='Interview Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["interview_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=dates["Acceptance Received"],
                               name='Acceptance Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["acceptance"],
                               opacity=0.75))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', bargap=0, margin=dict(l=0, r=0, t=0, b=0), height=200, autosize=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON