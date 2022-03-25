import math

def categorize_gpa(gpa):
    '''Returns a given GPA within a binned category.'''
    # Handle users who have not entered GPA
    if not gpa:
        return None

    if gpa >= 3.9:
        return "3.9+"
    elif gpa < 3.0:
        return "<3.0"
    else:
        # Truncate to nearest tenth
        gpa = math.trunc(gpa * 10) / 10
        return f'{gpa}-{gpa+0.1}'

def categorize_mcat(mcat):
    '''Returns a given MCAT score within a binned category.'''
    # Handle users who have not entered MCAT
    if not mcat:
        return None

    if mcat >= 520:
        return "520+"
    elif mcat < 500:
        return "<500"
    else:
        return f'{mcat-2}-{mcat+2}'