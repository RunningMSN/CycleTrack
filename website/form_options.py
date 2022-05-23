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

# GPA Calculator
GRADE_OPTIONS = ['A+', 'A', 'A-', 'AB', 'B+', 'B', 'B-', 'BC', 'C+', 'C', 'C-', 'CD', 'D+', 'D', 'D-', 'DE', 'DF', 'E',
                 'F', 'AP (Tested Out)', 'AU (Audit)', 'Currently Taking', 'CR (Credit)', 'P (Pass/Fail)',
                 'F (Pass/Fail)', 'W (Withdrawn)', 'EX (Exempt)', 'Future']

AMCAS_WEIGHT = {'A+': 4, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D+': 1.3,
                'D': 1, 'D-': 0.7, 'F': 0, 'AB': 3.5, 'BC': 2.5, 'CD': 1.5, 'DE': 0.5, 'DF': 0.5}

AACOMAS_WEIGHT = {'A+': 4, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D+': 1.3,
                  'D':1, 'D-': 0.7, 'F': 0, 'AB': 3.5, 'BC': 2.5, 'CD': 1.5, 'DE': 0.5, 'DF': 0.5}

TMDSAS_WEIGHT = {'A+': 4, 'A': 4, 'A-': 4, 'B+': 3, 'B': 3, 'B-': 3, 'C+': 2, 'C': 2, 'C-': 2, 'D+': 1,
                  'D': 1, 'D-': 1, 'F': 0, 'AB': 3.5, 'BC': 2.5, 'CD': 1.5, 'DE': 0.5, 'DF': 0.5}

COURSE_CLASSIFICATIONS = sorted(['Biology', 'Chemistry', 'Physics', 'Math', 'Behavioral/Social Science', 'Business',
                          'Computer Science/Technology', 'Education', 'Engineering', 'English', 'Fine Arts',
                          'Foreign Language', 'Government', 'Health Science', 'History', 'Natural/Physical Science',
                          'Other', 'Philosophy/Religion'])

AMCAS_SCIENCE = ['Biology', 'Chemistry', 'Physics', 'Math']

COURSE_TERMS = {0:'Summer', 1:'Fall', 2:'Winter', 3:'Spring'}

COURSE_YEARS = list(reversed([str(i) + '-' + str(i+1) for i in range(1950,VALID_CYCLES[0]+2)]))

PROGRAM_TYPES = ['Undergraduate', 'Post-bac', 'Graduate']

# Quarter conversion to semester hours
AMCAS_QUARTER_CONVERSION = {0.5:0.3, 1:0.7, 1.5:1, 2:1.3, 2.5:1.7, 3:2, 3.5:2.3, 4:2.7, 4.5:3, 5:3.3, 6:4,
                            7:4.7, 8:5.3, 9:6, 10:6.7, 12:8, 15:10, 20:13.3}