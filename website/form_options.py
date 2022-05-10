import pandas as pd
from . import db
from .models import School_Profiles_Data

# Cycles available to add data
VALID_CYCLES = [2023, 2022, 2021, 2020]
# Current cycle to be used for explorer pages
CURRENT_CYCLE = 2022

# List of schools for adding to profile
def get_md_schools(country = None):
    '''Returns list of all available MD schools'''
    if country == 'USA':
        md_schools = School_Profiles_Data.query.filter_by(md_or_do='MD', country='USA').all()
    elif country == 'CAN':
        md_schools = School_Profiles_Data.query.filter_by(md_or_do='MD', country='CAN').all()
    else:
        md_schools = School_Profiles_Data.query.filter_by(md_or_do='MD').all()
    names = sorted([school.school for school in md_schools])
    return names
def get_do_schools():
    '''Returns list of all available DO schools'''
    do_schools = School_Profiles_Data.query.filter_by(md_or_do='DO').all()
    names = sorted([school.school for school in do_schools])
    return names

# Options for cycle profile page
SEX_OPTIONS = ["Male", "Female", "Other"]
GENDER_OPTIONS = ["Male", "Female", "Trans Male", "Trans Female", "Genderqueer", "Other"]
RACE_ETHNICITY_OPTIONS = ["Hispanic/Latino/Spanish Origin", "American Indian/Alaskan Native", "Asian",
                          "Black/African American", "Native Hawaiian/Pacific Islander", "White"]
STATE_OPTIONS = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                 "District of Columbia", "Florida","Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
                 "Kansas", "Kentucky", "Louisiana", "Maine","Maryland", "Massachusetts", "Michigan", "Minnesota",
                 "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                 "New Mexico", "New York", "North Carolina", "North Dakota","Ohio","Oklahoma", "Oregon", "Pennsylvania",
                 "Rhode Island", "South Carolina", "South Dakota", "Tennessee","Texas", "Utah", "Vermont", "Virginia",
                 "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico", "Guam", "American Samoa",
                 "Canada", "International", "Other"]

# Settings for visualizations page
VIS_TYPES = ["Line", "Bar", "Dot", "Sankey","Map"]

# Settings for color palettes
COLOR_TYPES = ["Default","Okabe-Ito","Tol"]

# Settings for map scopes
MAP_TYPES = ["USA", "North America"]

# School list import column types
COLUMN_TYPES = ["School Name", "Primary Submitted/Verified", "Secondary Received",
                "Application Complete", "Interview Received", "Interview Date", "Rejected", "Waitlisted", "Accepted",
                "Withdrawn"]
COLUMN_LABEL_CONVERT_SQL = {"School Name": "name", "Primary Submitted/Verified": "primary",
                            "Secondary Received": "secondary_received",
                            "Application Complete": "application_complete", "Interview Received": "interview_received",
                            "Interview Date": "interview_date", "Rejected": "rejection", "Waitlisted": "waitlist",
                            "Accepted": "acceptance",
                            "Withdrawn": "withdrawn"}

# Explorer options
STATES_WITH_SCHOOLS = ["Alabama",  "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
                 "District of Columbia", "Florida","Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
                 "Kansas", "Kentucky", "Louisiana", "Maine","Maryland", "Massachusetts", "Michigan", "Minnesota",
                 "Mississippi", "Missouri", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                 "New Mexico", "New York", "North Carolina", "North Dakota","Ohio","Oklahoma", "Oregon", "Pennsylvania",
                 "Rhode Island", "South Carolina", "South Dakota", "Tennessee","Texas", "Utah", "Vermont", "Virginia",
                 "Washington", "West Virginia", "Wisconsin", "Puerto Rico"]

STATE_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Northwest Territories": "NT",
    "Nova Scotia": "NS",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT",
    "Canada": "CAN"
}

ABBREV_TO_STATE = dict(map(reversed, STATE_ABBREV.items()))