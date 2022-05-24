from .. import form_options

def amcas_gpa(courses, type='cumulative'):
    total_hours = 0
    total_score = 0

    for course in courses:
        if type=='science':
            if course.classification not in form_options.AMCAS_SCIENCE:
                continue
        elif type=='nonscience':
            if course.classification in form_options.AMCAS_SCIENCE:
                continue
        # Only include courses that are counted
        if course.grade in form_options.AMCAS_WEIGHT.keys() and course.program_type in ['Undergraduate', 'Post-bac']:
            # Bypass if not int
            if isinstance(course.credits, int) or isinstance(course.credits, float):
                # Account for quarters
                semester_hours = course.credits
                if course.quarter:
                    if course.credits in form_options.AMCAS_QUARTER_CONVERSION.keys():
                        semester_hours = form_options.AMCAS_QUARTER_CONVERSION[course.credits]
                    else:
                        semester_hours = form_options.AMCAS_QUARTER_CONVERSION[1] * semester_hours
                total_score = total_score + semester_hours * form_options.AMCAS_WEIGHT[course.grade]
                total_hours = total_hours + semester_hours
    if total_hours == 0:
        return 'NaN'
    else:
        return '{:.2f}'.format(total_score/total_hours)


def aacomas_gpa(courses, type='cumulative'):
    total_hours = 0
    total_score = 0

    for course in courses:
        if type=='science':
            if not course.aacomas_science:
                continue
        elif type=='nonscience':
            if course.aacomas_science:
                continue
        # Only include courses that are counted
        if course.grade in form_options.AACOMAS_WEIGHT.keys() and course.program_type in ['Undergraduate', 'Post-bac', 'Graduate']:
            # Bypass if not int
            if isinstance(course.credits, int) or isinstance(course.credits, float):
                # Account for quarters
                semester_hours = course.credits
                if course.quarter:
                    semester_hours = semester_hours * 0.667
                total_score = total_score + semester_hours * form_options.AACOMAS_WEIGHT[course.grade]
                total_hours = total_hours + semester_hours
    if total_hours == 0:
        return 'NaN'
    else:
        return '{:.2f}'.format(total_score/total_hours)

def tmdsas_gpa(courses, type='cumulative'):
    total_hours = 0
    total_score = 0

    for course in courses:
        if type=='science':
            if not course.tmdsas_science:
                continue
        elif type=='nonscience':
            if course.tmdsas_science:
                continue
        # Only include courses that are counted
        if course.grade in form_options.TMDSAS_WEIGHT.keys() and course.program_type in ['Undergraduate', 'Post-bac', 'Graduate']:
            # Bypass if not int
            if isinstance(course.credits, int) or isinstance(course.credits, float):
                # Account for quarters
                semester_hours = course.credits
                if course.quarter:
                    semester_hours = semester_hours * 0.667
                total_score = total_score + semester_hours * form_options.TMDSAS_WEIGHT[course.grade]
                total_hours = total_hours + semester_hours
    if total_hours == 0:
        return 'NaN'
    else:
        return '{:.2f}'.format(total_score/total_hours)