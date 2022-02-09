# Cycles to include in site
VALID_CYCLES = [2022, 2021, 2020]

# List of schools for adding to profile
MD_SCHOOL_LIST = sorted(
    ["Alabama", "South Alabama", "Arkansas", "Arizona", "Arizona Phoenix", "California", "California Northstate",
     "Kaiser Permanente", "Loma Linda", "Southern Cal-Keck", "Stanford", "UC Davis", "UC Irvine", "UC Riverside",
     "UC San Diego", "UC San Francisco", "UCLA-Geffen", "Colorado", "Connecticut", "Quinnipiac-Netter", "Yale",
     "George Washington", "Georgetown", "Howard", "FIU-Wertheim", "Florida", "Florida Atlantic-Schmidt",
     "Florida State", "Miami-Miller", "Nova Southeastern-Patel", "UCF", "USF-Morsani", "Emory", "MC Georgia Augusta",
     "Mercer", "Morehouse", "Hawaii-Burns", "Iowa-Carver", "Carle Illinois", "Chicago Med Franklin", "Chicago-Pritzker",
     "Illinois", "Loyola-Stritch", "Northwestern-Feinberg", "Rush", "Southern Illinois", "Indiana", "Kansas",
     "Kentucky", "Louisville", "LSU New Orleans", "LSU Shreveport", "Tulane", "Boston", "Harvard", "Massachusetts",
     "Tufts", "Johns Hopkins", "Maryland", "Uniformed Services-Hebert", "Central Michigan", "Michigan",
     "Michigan State", "Oakland Beaumont", "Wayne State", "Western Michigan-Stryker", "Mayo", "Minnesota",
     "Missouri Columbia", "Missouri Kansas City", "Saint Louis", "Washington U St Louis", "Mississippi", "Duke",
     "East Carolina-Brody", "North Carolina", "Wake Forest", "North Dakota", "Creighton", "Nebraska",
     "Dartmouth-Geisel", "Cooper Rowan", "Hackensack Meridian", "Rutgers New Jersey", "Rutgers-RW Johnson",
     "New Mexico", "Nevada Reno", "UNLV-Kerkorian", "Albany", "Buffalo-Jacobs", "CUNY", "Columbia-Vagelos",
     "Cornell-Weill", "Einstein", "Mount Sinai-Icahn", "NYU Long Island", "NYU-Grossman", "New York Medical",
     "Renaissance Stony Brook", "Rochester", "SUNY Downstate", "SUNY Upstate", "Zucker Hofstra Northwell",
     "Case Western Reserve", "Cincinnati", "Northeast Ohio", "Ohio State", "Toledo", "Wright State-Boonshoft",
     "Oklahoma", "Oregon", "Drexel", "Geisinger Commonwealth", "Jefferson-Kimmel", "Penn State",
     "Pennsylvania-Perelman", "Pittsburgh", "Temple-Katz", "Caribe", "Ponce", "Puerto Rico", "San Juan Bautista",
     "Brown-Alpert", "MU South Carolina", "South Carolina Columbia", "South Carolina Greenville",
     "South Dakota-Sanford", "East Tennessee-Quillen", "Meharry", "Tennessee", "Vanderbilt", "Baylor", "Houston",
     "TCU UNTHSC", "Texas A & M", "Texas Tech", "Texas Tech-Foster", "UT Austin-Dell", "UT Houston-McGovern",
     "UT Medical Branch", "UT Rio Grande Valley", "UT San Antonio-Long", "UT Southwestern", "Utah", "Eastern Virginia",
     "Virginia", "Virginia Commonwealth", "Virginia Tech Carilion", "Vermont-Larner", "U Washington",
     "Washington State-Floyd", "MC Wisconsin", "Wisconsin", "Marshall-Edwards", "West Virginia"])
DO_SCHOOL_LIST = sorted(['Alabama College of Osteopathic Medicine',
                         'Arizona College of Osteopathic Medicine of Midwestern University',
                         'Arkansas College of Osteopathic Medicine',
                         'A.T. Still University-Kirksville College of Osteopathic Medicine',
                         'A.T. Still University-School of Osteopathic Medicine in Arizona',
                         'Burrell College of Osteopathic Medicine at New Mexico State University',
                         'California Health Sciences University College of Osteopathic Medicine',
                         'Campbell University Jerry M. Wallace School of Osteopathic Medicine',
                         'Chicago College of Osteopathic Medicine of Midwestern University',
                         'Des Moines University College of Osteopathic Medicine',
                         'Idaho College of Osteopathic Medicine',
                         'Kansas City University College of Osteopathic Medicine',
                         'Kansas Health Science Center - Kansas College of Osteopathic Medicine',
                         'Lake Erie College of Osteopathic Medicine',
                         'Liberty University College of Osteopathic Medicine',
                         'Lincoln Memorial University - DeBusk College of Osteopathic Medicine',
                         'Marian University College of Osteopathic Medicine',
                         'Michigan State University College of Osteopathic Medicine',
                         'New York Institute of Technology College of Osteopathic Medicine',
                         'Noorda College of Osteopathic Medicine',
                         'Nova Southeastern University Dr. Kiran C. Patel College of Osteopathic Medicine',
                         'Ohio University Heritage College of Osteopathic Medicine',
                         'Oklahoma State University Center for Health Sciences College of Osteopathic Medicine',
                         'Pacific Northwest University of Health Sciences College of Osteopathic Medicine',
                         'Philadelphia College of Osteopathic Medicine',
                         'Philadelphia College of Osteopathic Medicine Georgia Campus',
                         'Rocky Vista University College of Osteopathic Medicine',
                         'Rowan University School of Osteopathic Medicine',
                         'Sam Houston State University College of Osteopathic Medicine',
                         'Touro College of Osteopathic Medicine - New York',
                         'Touro University College of Osteopathic Medicine - California',
                         'Touro University Nevada College of Osteopathic Medicine',
                         'University of the Incarnate Word School of Osteopathic Medicine',
                         'University of New England College of Osteopathic Medicine',
                         'University of North Texas Health Science Center at Fort Worth - Texas College of Osteopathic Medicine',
                         'University of Pikeville - Kentucky College of Osteopathic Medicine',
                         'Edward Via College of Osteopathic Medicine - Auburn Campus',
                         'Edward Via College of Osteopathic Medicine - Carolinas Campus',
                         'Edward Via College of Osteopathic Medicine - Louisiana Campus',
                         'Edward Via College of Osteopathic Medicine - Virginia Campus',
                         'West Virginia School of Osteopathic Medicine',
                         'Western University of Health Sciences College of Osteopathic Medicine of the Pacific',
                         'William Carey University College of Osteopathic Medicine'])

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
VIS_TYPES = ["Line", "Bar", "Dot", "Sankey"]

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
