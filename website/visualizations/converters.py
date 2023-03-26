import pandas as pd
import datetime as dt
import numpy as np
from ..models import School_Profiles_Data
from .. import db

palette = {
    "default" : {'primary': '#90e0ef', 'secondary_received': '#00b4d8', 'application_complete': '#0077b6',
                  'interview_received': '#9932CC', 'interview_date': '#8B008B', 'rejection': '#FF0000',
                  'waitlist': '#FFA500', 'acceptance': '#008000', 'withdrawn': '#808080'},
    "okabe-ito" : {'primary': '#F0E442', 'secondary_received': '#56B4E9', 'application_complete': '#0072B2',
                  'interview_received': '#E69F00', 'interview_date': '#CC79A7', 'rejection': '#7a7a7a',
                  'waitlist': '#de91ff', 'acceptance': '#009E73', 'withdrawn': '#000000'},
    "tol" : {"primary":"#ddcc77","secondary_received":"#88ccee","application_complete":"#331888",
                "interview_received":"#882255","interview_date":"#117733","rejection":"#aa4499",
                "waitlist":"#cc6677","acceptance":"#44aa99","withdrawn":"#000000"}
}


action_names = {'primary': 'Primary Submitted', 'secondary_received': 'Secondary Received', 'application_complete': 'Application Complete',
                  'interview_received': 'Interview Received', 'interview_date': 'Interview Complete', 'rejection': 'Rejection',
                  'waitlist': 'Waitlist', 'acceptance': 'Acceptance', 'withdrawn': 'Withdrawn'}

                  
action_weight = {
    'primary': 0,
    'secondary_received': 1, 
    'application_complete': 2,
    'interview_received':3, 
    'interview_date': 4, 
    'rejection': 5,
    'waitlist': 6,
    'acceptance': 7, 
    'withdrawn': 8
}

def convert_sums(data):
    # Store numbers of each action on each date
    dicts = []
    # Collect the dates and numbers of actions
    for column in data.columns:
        if column != data.columns[0]:
            # Gather number of actions at each date for every type of action
            temp_dict = {}
            for date in data[column]:
                # Get number of actions per date
                if not pd.isnull(date):
                    temp_dict[date] = sum(data[column] <= date)
            dicts.append(temp_dict)

    # Get column names based on number user supplied
    column_names = {}
    for i in range(0, len(data.columns[1:])):
        column_names[i] = data.columns[1:][i]

    # Generate data frame
    cleaned_data = pd.DataFrame(dicts).T
    cleaned_data = cleaned_data.rename(column_names, axis=1)
    # Add starting point
    cleaned_data.loc[min(cleaned_data.index) - dt.timedelta(1)] = [0 for i in range(0, len(column_names))]
    cleaned_data = cleaned_data.sort_index()
    # Fill in any missing days
    cleaned_data = cleaned_data.reindex(pd.date_range(start=min(cleaned_data.index), end=max(cleaned_data.index)))
    # Fill in missing data and drop unnamed columns
    cleaned_data = cleaned_data.ffill()
    cleaned_data = cleaned_data.loc[:, ~cleaned_data.columns.str.contains("Unnamed")]
    return cleaned_data

def convert_bar_df(data):
    # Remove potentially future interview dates if withdrawn
    data["interview_date"] = data.apply(
        lambda row: row["interview_date"] if row["interview_date"] <= row["withdrawn"] else np.nan, axis=1)

    # Obtain a range of all dates
    melted = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='actions', value_name='date')
    start_dates = min(melted['date'].dropna())
    end_dates = max(melted['date'].dropna())
    all_dates = pd.date_range(start=start_dates, end=end_dates)

    # Remove names
    names_removed = data.drop('name', axis=1)
    # Reverse order of columns for cases of 2 equal dates
    names_removed = names_removed[names_removed.columns[::-1]]

    # Generate initial dataframe to add to
    output = pd.DataFrame()
    output['Best Outcome'] = names_removed[names_removed <= all_dates[0]].dropna(axis=0, how='all').idxmax(axis=1)
    output['Date'] = all_dates[0]
    # Continue adding for all dates
    for date in all_dates[1:]:
        df = pd.DataFrame()
        df['Best Outcome'] = names_removed[names_removed <= date].dropna(axis=0, how='all').idxmax(axis=1)
        df['Date'] = date
        output = pd.concat([output,df])

    # Get counts for all dates
    output = output.groupby(['Date', 'Best Outcome']).size().reset_index(name='Count')

    return output

def sankey_build_frames(cycle_data,color="default"):
    df_nodes = {'label': cycle_data.columns}
    df_nodes = pd.DataFrame(df_nodes)
    ids = {}
    fig_colors = palette[color]
    for i in range(0, len(df_nodes['label'])):
        ids[df_nodes['label'][i]] = i
    df_nodes['color'] = df_nodes.apply(lambda row: fig_colors[row.label], axis=1)
    df_nodes['label'] = df_nodes.apply(lambda row: action_names[row.label], axis=1)
    out = {'Source': [], 'Target': [], 'Link Color': []}
    for index, row in cycle_data.iterrows():
        row_sorted = row.dropna().sort_values()
        for i in range(0, len(row_sorted)):
            if i == len(row_sorted) - 1:
                break
            else:
                out['Source'].append(ids[row_sorted.index[i]])
                out['Target'].append(ids[row_sorted.index[i + 1]])
                h = fig_colors[row_sorted.index[i + 1]].lstrip('#')
                col = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
                col = list(col)
                col.append(0.5)
                col = tuple(col)
                out['Link Color'].append(f'rgba{col}')
    df_links = pd.DataFrame(out)
    df_links = df_links.groupby(df_links.columns.tolist(), as_index=False).size()

    full_labels = []
    for key, value in ids.items():
        if key == cycle_data.columns[0]:
            full_labels.append(f'{action_names[key]}: {str(sum(df_links[df_links["Source"] == value]["size"]))}')
        else:
            full_labels.append(f'{action_names[key]}: {str(sum(df_links[df_links["Target"] == value]["size"]))}')
    df_nodes['label'] = full_labels
    return df_nodes, df_links


def convert_map(data,color="default"):
    fig_colors = palette[color]
    #merge schools so that the most recent decision for a school counts
    #(aka MD + MD/PhD don't get put in twice)
    cols = (data.columns[::-1]).tolist()
    data = data.sort_values(by=cols).groupby("name",as_index=False).last()
    for ind,row in data[data.columns.difference(["name"])].iterrows():
        if row.isnull().all():
            data = data.drop(index=ind)
    #get best outcome: column with greatest date in each row
    nameless = data[data.columns.difference(["name"])]
    data["Best Outcome"] = nameless.idxmax(axis=1)
    data["color"] = data["Best Outcome"].map(fig_colors)
    #merge with school locations
    school_df = data[["name","Best Outcome","color"]]
    school_df = school_df.rename(columns={"name":"school"})
    profiles = pd.read_sql(School_Profiles_Data.query.statement, db.session.bind)
    loc_df = school_df.merge(profiles, how="left", on="school")

    return loc_df

def convert_horz_bar(data,cycleyear):
    print(data['secondary_received'])
    data['secondary_received'] = data['secondary_received'] + dt.timedelta(seconds = 1)
    data['application_complete'] = data['application_complete'] + dt.timedelta(seconds=2)
    temp_melt = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='Actions', value_name='date')
    cycle_max = temp_melt["date"].max()
    today = dt.date.today()
    if dt.date(today.year,8,31) <= dt.date(cycleyear-1,8,31):
        last_date = dt.date(cycleyear,8,31)
    else:
        last_date = today
    after_last = temp_melt["date"].max() + dt.timedelta(days=1)
    data['today'] = last_date
    melted = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='Actions', value_name='date')
    schools = melted["name"].unique()
    dfs = []
    melted = melted.sort_values(by="date")
    for school in schools:
        melt_copy = melted.copy()
        melt_copy = melt_copy.dropna()
        actions = melt_copy.loc[melted["name"]==school,"Actions"].unique()
        
        #if there are dates in the future, allow it for only 1 school
        if actions[-1] != "today":
            actions = np.delete(actions, np.argwhere(actions == "today"))
            data['after_last'] = after_last
            actions = np.append(actions,'after_last')

        for action1,action2 in zip(actions,actions[1:]):
            df = data.loc[data["name"]==school,["name",action1,action2]]
            df["label"] = action1
            df["label2"] = action_names[action1]
            df.columns = ["name","start","stop","Outcome","label2"]
            dfs.append(df)
    
    concat_df = pd.concat(dfs)

    return concat_df