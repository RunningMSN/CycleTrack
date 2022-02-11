# Cycles to include in site
VALID_CYCLES = [2022, 2021, 2020]

# List of schools for adding to profile
import pandas as pd
profiles = pd.read_csv("./website/static/csv/SchoolProfiles.csv")
MD_SCHOOL_LIST = list(profiles.loc[profiles["MD_or_DO"]=="MD"]["School"])
DO_SCHOOL_LIST = list(profiles.loc[profiles["MD_or_DO"]=="DO"]["School"])

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
