from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import flash
import dateutil.parser
import jellyfish
import re

school_nicknames_dict = pd.read_csv('./website/static/csv/school_names_nicknames.csv').set_index('Key').to_dict()['Value']

def read_google(link):
    '''Converts a google sheets link to a pandas dataframe.'''
    if len(link) > 0 and link.endswith("pubhtml"):
        page = requests.get(link).text
        soup = BeautifulSoup(page, "html.parser")
        # List that holds each row as a list
        input_data = []
        for row in soup.find_all('tr'):
            # List of elements in the row
            row_data = []
            for element in row.find_all('td'):
                if len(element.get_text()) > 0:
                    row_data.append(element.get_text())
                else:
                    row_data.append(None)
            input_data.append(row_data)
        column_names = [str(name) for name in input_data[1]]
        # Convert list to DataFrame and return
        df = convert_columns_date(pd.DataFrame(input_data[2:], columns=column_names))
        # Drop problematic rows with all null
        df = df.dropna(how='all', axis=0)
        return df
    else:
        flash('Please make sure your google sheet has been published to the web.', category='error')

def convert_columns_date(df):
    '''Converts imported spreadsheet data frames into datetime.'''
    for index, row in df.iterrows():
        for item in row.keys()[1:]:
            if type(row[item]) is str:
                if len(row[item]) == 0:
                    row[item] = None
                else:
                    row[item] = dateutil.parser.parse(row[item])
            else:
                if not pd.isnull(row[item]):
                    row[item] = pd.to_datetime(row[item], unit='ms')
                else:
                    row[item] = None
        df.loc[index] = row
    return df


def best_match(input_string, match_list, cutoff):
    '''Returns the closest match to the input string from the match list. If no matches above cutoff, returns none.'''
    # For matching purpose, remove PhD labels
    phd_labels = ['mstp', 'md-phd', 'md/phd', 'mdphd', 'do-phd', 'do/phd', 'dophd']
    for label in phd_labels:
        if label in input_string.lower():
            pattern = re.compile(label, re.IGNORECASE)
            input_string = pattern.sub("", input_string).strip()
            break

    # Check if native input already in the list
    if input_string in match_list:
        return input_string

    # Store best match
    best_score = 0
    best_match = ""
    for value in match_list:
        score = jellyfish.jaro_distance(input_string, value)
        if score > best_score:
            best_match = value
            best_score = score

    if best_score >= cutoff:
        return best_match
    else:
        return None