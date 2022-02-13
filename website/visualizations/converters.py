import pandas as pd
import datetime as dt

fig_colors = {'primary': '#90e0ef', 'secondary_received': '#00b4d8', 'application_complete': '#0077b6',
                  'interview_received': '#9932CC', 'interview_date': '#8B008B', 'rejection': '#FF0000',
                  'waitlist': '#FFA500', 'acceptance': '#008000', 'withdrawn': '#808080'}

action_names = {'primary': 'Primary Submitted', 'secondary_received': 'Secondary Received', 'application_complete': 'Application Complete',
                  'interview_received': 'Interview Received', 'interview_date': 'Interview Complete', 'rejection': 'Rejection',
                  'waitlist': 'Waitlist', 'acceptance': 'Acceptance', 'withdrawn': 'Withdrawn'}

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
    # Obtain a range of all dates
    melted = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='actions', value_name='date')
    start_dates = min(melted['date'].dropna())
    end_dates = max(melted['date'].dropna())
    all_dates = pd.date_range(start=start_dates, end=end_dates)

    # Remove names
    names_removed = data.drop('name', axis=1)

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

def sankey_build_frames(cycle_data):
    df_nodes = {'label': cycle_data.columns}
    df_nodes = pd.DataFrame(df_nodes)
    ids = {}
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

    return df_nodes, df_links

#I name this dataframe a little differently in the form_options script. may want to unify
locations = pd.read_csv("./website/static/csv/SchoolProfiles.csv")

def convert_map(data,aggregate=False):
    if aggregate:
        school_df = data[["name"]]
    else:
        #merge schools so that duplicates (aka MD + MD/PhD don't get put in twice)
        data = data.groupby("name",as_index=False).first()
        #get best outcome: column with greatest date in each row
        nameless = data[data.columns.difference(["name"])]
        data["Best Outcome"] = nameless.idxmax(axis=1)
        data["color"] = data["Best Outcome"].map(fig_colors)
        #merge with school locations
        school_df = data[["name","Best Outcome","color"]]

    school_df = school_df.rename(columns={"name":"School"})
    loc_df = school_df.merge(locations,how="left",on="School")

    return loc_df