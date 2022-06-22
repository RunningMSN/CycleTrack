from . import bar, horz_bar

def public_bar(data,title):

    graphJSON = bar.generate(data, title, False, color="default",custom_text=None)
    return graphJSON

def public_timeline(data,title):
    graphJSON = horz_bar.generate(data, title, False, color="default",custom_text=None,hide_school_names=False)
    return graphJSON