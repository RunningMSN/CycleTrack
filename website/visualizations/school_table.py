import pandas as pd

def generate(school):
    school_profiles = pd.read_csv('website/static/csv/SchoolProfiles2.csv')
    mask = school_profiles["School"] == school
    school_df = school_profiles[mask]
    order = [
        'md_apps_all', 'md_apps_is',  'md_apps_oos','md_apps_men','md_apps_women', 
        'md_mats_all', 'md_mats_is', 'md_mats_oos','md_mats_men', 'md_mats_women', 
        'md_mats_rate', 
        'mdphd_apps_all','mdphd_apps_is', 'mdphd_apps_oos', 'mdphd_apps_men', 'mdphd_apps_women',
       'mdphd_mats_all', 'mdphd_mats_is', 'mdphd_mats_oos','mdphd_mats_men', 'mdphd_mats_women',
       'mdphd_mats_rate', ]
    school_df = school_df[order]
    df = school_df.columns.to_series().str.split("_",expand=True)
    school_df.columns = pd.MultiIndex.from_arrays([df[0].to_list(),df[1].to_list(),df[2].to_list()])
    school_df = school_df.rename({"md":"MD","mdphd":"MD/PhD",
    "apps":"Applications", "mats":"Matriculants",
    "all":"#","is":"In-State (%)","oos":"Out-of-State (%)",
    "men":"Men (%)","women":"Women (%)",
    "rate":"Rate (%)"},axis=1)

    md_html = school_df["MD"].to_html(index=False,justify="center",classes = "table table-bordered")

    mdphd_html = school_df["MD/PhD"].to_html(index=False,justify="center",classes = "table table-bordered")

    return md_html,mdphd_html