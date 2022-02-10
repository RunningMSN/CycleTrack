#name matching for MD schools
import pandas as pd
import re
import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import jellyfish


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

clean_list = [s.replace('-', ' ') for s in MD_SCHOOL_LIST]

limey_list = list(pd.read_csv("https://raw.githubusercontent.com/ijhua/aamc_admissions/main/processed_files/schoolinfo.csv")["name"].dropna())
aamc_list = list(pd.read_csv("https://raw.githubusercontent.com/ijhua/aamc_admissions/main/processed_files/schoolinfo.csv")["school"].dropna())

def fuzzy_match(name,list_names,min_score=0):
    fuzzy_choices = process.extract(name,list_names,scorer=fuzz.token_sort_ratio)
    
    fuzzy_choice = fuzzy_choices[0]

    if fuzzy_choice[1] > min_score:
        max_name = fuzzy_choice[0]
        score = fuzzy_choice[1]
    else:
        max_name = ""
        score = -1
    return (max_name, score)

def fish_match(name,list_names,min_score=0):
    max_score = -1
    max_name = ""
    for x in list_names:
        current_score = jellyfish.jaro_distance(name,x)*100
        if (current_score > min_score) & (current_score > max_score):
            max_score = current_score
            max_name = x
    return (max_name,max_score)

def fuzzy_or_fish(name, list_names,min_score):
    fuzzy_best = fuzzy_match(name,list_names,min_score)
    fish_best = fish_match(name,list_names,min_score)
    print(fish_best)
    if fish_best[1] > fuzzy_best[1]:
        print("fish best")
        best_match = fish_best
    elif fuzzy_best[1] > fish_best[1]:
        print("fuzzy best")
        best_match = fuzzy_best
    else:
        print("equally good?")
        best_match = fish_best
    return best_match

names = []
'''for x in MD_SCHOOL_LIST:
    match = match_names(x,school_names,65)
    print(x,match)
    name = (f"{x}",f"{match[0]}")
    names.append(name)
name_dict = dict(names)
print(name_dict)'''


# testing the functions out
test_list = ["UCSD","UC SD","WashU", "University of Washington"," UW","Franklin", "Buffalo-Jacobs","Texas AM"]

for x in test_list:
    print(x)
    match = fuzzy_or_fish(x,aamc_list,65)
    print(x,match)
    name = (f"{x}",f"{match[0]}")
    names.append(name)
name_dict = dict(names)
print(name_dict)