import pandas as pd
import numpy as np

a1_new = "https://github.com/ijhua/aamc_live/blob/main/processing/data/A-1/2021_FACTS_Table_A-1.xlsx?raw=true"
b8_new = "https://github.com/ijhua/aamc_live/blob/main/processing/data/B-8/2021_FACTS_Table_B-8.xlsx?raw=true"

heads = [4,5,6,7]
md_column_names = ["state","school",
"md_apps_all","md_apps_is","md_apps_oos","md_apps_women","md_apps_men",
"md_mats_all","md_mats_is","md_mats_oos","md_mats_women","md_mats_men"]

mdphd_column_names = ["state","school",
"mdphd_apps_all","mdphd_apps_is","mdphd_apps_oos","mdphd_apps_women","mdphd_apps_men",
"mdphd_mats_all","mdphd_mats_is","mdphd_mats_oos","mdphd_mats_women","mdphd_mats_men"]

a1 = pd.read_excel(a1_new,header = heads)
a1.columns = md_column_names
a1 = a1[a1['md_apps_all'].notna()]
a1["state"] = a1["state"].fillna(method="ffill")
a1["school"] = a1["school"].str.replace('\d+', '',regex=True)
a1 = a1[~a1.state.str.contains("Total")]
a1["md_mats_rate"] = round((a1["md_mats_all"]/a1["md_apps_all"])*100,2)
a1 = a1.replace({np.inf:0})


b8 = pd.read_excel(b8_new,header = heads)
b8.columns = mdphd_column_names
b8 = b8[b8['mdphd_apps_all'].notna()]
b8["state"] = b8["state"].fillna(method="ffill")
b8["school"] = b8["school"].str.replace('\d+', '',regex=True)
b8 = b8[~b8.state.str.contains("Total")]
b8["mdphd_mats_rate"] = round((b8["mdphd_mats_all"]/b8["mdphd_apps_all"])*100,2)
b8 = b8.replace({np.inf:0})


data = a1.merge(b8,on=["state","school"],how="outer")

#name conversion
name_df = pd.read_csv("./website/static/csv/aamc_name_conv.csv",header=None)
name_df.columns = ["school","School"]

conv_df = name_df.merge(data,on=["school"])
conv_df = conv_df[conv_df.columns.difference(["school","state"])]

prof_df = pd.read_csv("./website/static/csv/SchoolProfiles.csv")
new_profiles = prof_df.merge(conv_df,on="School",how="outer")
new_profiles.to_csv("./website/static/csv/SchoolProfiles2.csv")