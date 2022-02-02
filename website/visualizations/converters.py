import pandas as pd
import datetime as dt

def convert_sums(data):
    # Store numbers of each action on each date
    dicts = []
    # Collect the dates and numbers of actions
    for column in data.columns:
        if column != data.columns[0]:
            # Convert to date time
            try:
                data[column] = pd.to_datetime(data[column])
            except:
                print(f"Error: some of your dates are not formatted correctly in {column}")

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