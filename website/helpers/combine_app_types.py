import pandas as pd


def combine(data):
    data['phd_str'] = data['phd'].apply(lambda x: '-PhD' if x else '')
    data["name"]  = data["name"] + " (" + data["school_type"] + data["phd_str"]+")"
    data.drop(['phd_str'],axis=1,inplace=True)
    return data