import pandas as pd
import datetime as dt
import numpy as np

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
