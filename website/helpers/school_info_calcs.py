import statistics

def interview_calculations(df, output_dict):
    # Interview Count
    output_dict['interview_count'] = len(df['interview_received'].dropna())
    # Percent of applicants who complete app interviewed
    apps_interview = df[['application_complete', 'interview_received']].dropna(how='all')
    apps_interview = apps_interview[apps_interview['application_complete'].notna()] # Ignore people who didn't fill in app complete
    output_dict['n_percent_interviewed'] = len(apps_interview)
    if len(apps_interview['application_complete']) > 0:
        output_dict['percent_interviewed'] = "{:.2f}%".format(len(apps_interview['interview_received'].dropna()) / len(apps_interview['application_complete'].dropna()) * 100)
    else:
        output_dict['percent_interviewed'] = None
    # cGPA
    interviewed_cgpa = df[['interview_received', 'cgpa']].dropna(how='any')['cgpa']
    output_dict['n_interviewed_cgpa'] = len(interviewed_cgpa)
    if len(interviewed_cgpa) > 0:
        output_dict['interviewed_cgpa'] = f'{statistics.median(interviewed_cgpa):.2f} ({min(interviewed_cgpa):.2f} - {max(interviewed_cgpa):.2f})'
    else:
        output_dict['interviewed_cgpa'] = None
    # sGPA
    interviewed_sgpa = df[['interview_received', 'sgpa']].dropna(how='any')['sgpa']
    output_dict['n_interviewed_sgpa'] = len(interviewed_sgpa)
    if len(interviewed_sgpa) > 0:
        output_dict['interviewed_sgpa'] = f'{statistics.median(interviewed_sgpa):.2f} ({min(interviewed_sgpa):.2f} - {max(interviewed_sgpa):.2f})'
    else:
        output_dict['interviewed_sgpa'] = None
    # MCAT
    interviewed_mcat = df[['interview_received', 'mcat_total']].dropna(how='any')['mcat_total']
    output_dict['n_interviewed_mcat'] = len(interviewed_mcat)
    if len(interviewed_mcat) > 0:
        output_dict['interviewed_mcat'] = f'{statistics.median(interviewed_mcat):.1f} ({min(interviewed_mcat):.1f} - {max(interviewed_mcat):.1f})'
    else:
        output_dict['interviewed_mcat'] = None

def acceptance_calculations(df, output_dict):
    # Acceptance Count
    output_dict['acceptance_count'] = len(df['acceptance'].dropna())
    # Percent of applicants interviewed and accepted
    apps_accepted = df[df['interview_received'].notna()].dropna(how='all')
    output_dict['n_percent_interview_accepted'] = len(apps_accepted)
    if len(apps_accepted['interview_received']) > 0:
        output_dict['percent_interview_accepted'] = "{:.2f}%".format(len(apps_accepted['acceptance'].dropna()) / len(apps_accepted['interview_received'].dropna()) * 100)
    else:
        output_dict['percent_interview_accepted'] = None
    # Percent of applicants waitlisted and accepted
    apps_accepted_waitlist = df[df['waitlist'].notna()].dropna(how='all')
    output_dict['n_percent_waitlist_accepted'] = len(apps_accepted_waitlist)
    if len(apps_accepted_waitlist['waitlist']) > 0:
        output_dict['percent_waitlist_accepted'] = "{:.2f}%".format(
            len(apps_accepted_waitlist['acceptance'].dropna()) / len(apps_accepted_waitlist['waitlist'].dropna()) * 100)
    else:
        output_dict['percent_waitlist_accepted'] = None
    # cGPA
    accepted_cgpa = df[['acceptance', 'cgpa']].dropna(how='any')['cgpa']
    output_dict['n_accepted_cgpa'] = len(accepted_cgpa)
    if len(accepted_cgpa) > 0:
        output_dict['accepted_cgpa'] = f'{statistics.median(accepted_cgpa):.2f} ({min(accepted_cgpa):.2f} - {max(accepted_cgpa):.2f})'
    else:
        output_dict['accepted_cgpa'] = None
    # sGPA
    accepted_sgpa = df[['acceptance', 'sgpa']].dropna(how='any')['sgpa']
    output_dict['n_accepted_sgpa'] = len(accepted_sgpa)
    if len(accepted_sgpa) > 0:
        output_dict['accepted_sgpa'] = f'{statistics.median(accepted_sgpa):.2f} ({min(accepted_sgpa):.2f} - {max(accepted_sgpa):.2f})'
    else:
        output_dict['accepted_sgpa'] = None
    # MCAT
    accepted_mcat = df[['acceptance', 'mcat_total']].dropna(how='any')['mcat_total']
    output_dict['n_accepted_mcat'] = len(accepted_mcat)
    if len(accepted_mcat) > 0:
        output_dict['accepted_mcat'] = f'{statistics.median(accepted_mcat):.1f} ({min(accepted_mcat):.1f} - {max(accepted_mcat):.1f})'
    else:
        output_dict['accepted_mcat'] = None