#%%
import pandas as pd
import matplotlib.pyplot as plt
# %%
df2018 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2018.csv')
df2019 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2019.csv')
df2020 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2020.csv')
df2021 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2021.csv')
df2022 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2022.csv')
df2023 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2023.csv')
df2024 = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/crashes_2024.csv')
# %%
#concat the crash data for every year
df = pd.concat([df2018, df2019, df2020, df2021, df2022, df2023, df2024])
# %%
#drop city since we are only looking at Austin data
df = df.drop(['City','Contributing Factors','Manner of Collision', 'Crash Time', 'Vehicle Body Style', 'Charge', 'Driver License Type', 'Person Alcohol Result', 'Person Drug Test Result'], axis=1)
df
# %%
print(df.dtypes)
# %%
df['Crash Date'] = pd.to_datetime(df['Crash Date'])
print(df.dtypes)
# %%
df['Year'] = df['Crash Date'].dt.year
# %%
df
# %%
#checking all values have the same format and the counts for each
unit_type_counts = df['Unit Description'].value_counts()
unit_type_counts
# %%
#pattern to clean format, i.e get rid of everything but the alpha characters inluding a space for multi word alpha text
#pattern = r'([A-Za-z]+(?:\s[A-Za-z]+)*)'
#?: non-capturing group
#(?i) makes pattern case insensitive specifically for "No Data"
#\w any single alphanumeric character
# \s*-\s* handles white space aroun dash
# (.*) captures everything after the dash
# |'No data' if pattern does not match then it matches exactly "no data" case insensitive 
#[0] extracts the first matched group
pattern = r'(?i)(?:\w\s*-\s*(.*)|(^No data$))'
# %%
df['Unit Description'].value_counts()
# %%
df['Unit Description'] = df['Unit Description'].str.extract(pattern)[0].fillna(df['Unit Description'])
#check new format
df['Unit Description'].value_counts()
# %%
df['Crash Severity'].value_counts()
#remove numerical code
df['Crash Severity'] = df['Crash Severity'].str.extract(pattern)[0].fillna(df['Crash Severity'])
#check new format
df['Crash Severity'].value_counts()
# %%
#remove numerical code
df['Person Ethnicity'].value_counts()
# %%
df['Person Ethnicity'] = df['Person Ethnicity'].str.extract(pattern)[0].fillna(df['Person Ethnicity'])
df['Person Ethnicity'].value_counts()
# %%
df['Person Gender'].value_counts()
df['Person Gender'] = df['Person Gender'].str.extract(pattern)[0].fillna(df['Person Gender'])
df['Person Gender'].value_counts()
# %%
df['Person Type'].value_counts()
df['Person Type'] = df['Person Type'].str.extract(pattern)[0].fillna(df['Person Type'])
df['Person Type'].value_counts()
# %%
df['Unit Description'].value_counts()
# %%
#dropping these type of crashes since they make up less than 1% of all crashes
less_than_1p_cent = df[(df['Unit Description'] == 'TOWED/PUSHED/TRAILER') | (df['Unit Description'] == 'MOTORIZED CONVEYANCE') | (df['Unit Description'] == 'NON-CONTACT')  |  
(df['Unit Description'] == 'OTHER  (EXPLAIN IN NARRATIVE)')  | 
(df['Unit Description'] == 'TRAIN')].index
# %%
df.drop(less_than_1p_cent, inplace = True) 
# %%
#looking at data after dropped values
df
#%%
# %%
df['Month Year'] = df['Crash Date'].dt.strftime('%B %Y')
df['Month Year']
# %%
#Get the start of the weeks, i.e Monday
df['Week Start'] = df['Crash Date'] - pd.to_timedelta(df['Crash Date'].dt.weekday, unit = 'D')
# %%
df['Week Start']
# %%
df.to_csv('cleanned_transformed.csv', index=False)
# %%
