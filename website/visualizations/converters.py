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

def convert_bar_df(data):
    # Obtain a range of all dates
    start_dates = pd.to_datetime('1/1/2100',format='%m/%d/%Y')
    end_dates = pd.to_datetime('1/1/1901',format='%m/%d/%Y')
    for column in data.columns[1:]:
        column_dates = data[column].dropna()
        if min(column_dates) < start_dates:
            start_dates = min(column_dates)
        if max(column_dates) > end_dates:
            end_dates = max(column_dates)
    all_dates = pd.date_range(start=start_dates, end=end_dates)

    # Order the statuses by priority with higher status having a smaller value
    status_order = {'withdrawn' : 0, 'acceptance' : 1, 'rejection' : 2, 'waitlist' : 3, 'interview_date' : 4,
                    'interview_received' : 5, 'application_complete' : 6, 'secondary_received' : 7, 'primary' : 8}

    # Assign schools the highest status for each date
    output = []
    # Iterate through possible dates
    for date in all_dates:
        # Iterate through the schools
        for index, row in data.iterrows():
            # Go through the statuses in order of priority
            for key, value in status_order.items():
                # Checks that user has this type of status
                if key in data.columns:
                    # Stops at first status
                    if not pd.isnull(row[key]) and date >= row[key]:
                        output.append([date, key])
                        break
    output_df = pd.DataFrame(output, columns=['Date', 'Best Outcome'])

    # Create dataframe with counts per status per date
    return output_df.groupby(['Date', 'Best Outcome']).size().reset_index(name='Count')
