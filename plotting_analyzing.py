#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
# %%
df = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/cleanned_transformed.csv')
# %%
df
# %%
#grouping and counting unique type crashes every year, renaming column and making year the index
yearly_type_counts = df.groupby(['Year','Unit Description'])['Crash ID'].nunique().reset_index()
yearly_type_counts.rename(columns={'Crash ID': 'Crash Count'}, inplace=True)
yearly_type_counts.set_index('Year', inplace=True)
yearly_type_counts
# %%
#pivoting so i can trend each unit type
df_pivot = yearly_type_counts.pivot_table(values='Crash Count', index=yearly_type_counts.index, columns='Unit Description')
# %%
#filtering data to only include deaths
filtered_df = df[df['Crash Death Count'] > 0]
# %%
#grouping deathly crashes by unit type, renaming column, and setting year as index
death_yearly_type_counts = filtered_df.groupby(['Year','Unit Description'])['Crash ID'].nunique().reset_index()
death_yearly_type_counts.rename(columns={'Crash ID': 'Death Count'}, inplace=True)
death_yearly_type_counts.set_index('Year', inplace=True)
# %%
df_death_pivot = death_yearly_type_counts.pivot_table(values='Death Count', index=death_yearly_type_counts.index, columns='Unit Description')
# %%
#editing crash count plot
plt.figure(figsize=(10, 6))
for col in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[col], marker='o', label=col)
    
plt.xlabel('Year')
plt.ylabel('Crash Count')
plt.title('Yearly Crash Count per Unit Type')
plt.legend(title='Unit Type')
plt.grid(True)
plt.show
# %%
#editing death plot
plt.figure(figsize=(10, 6))
for col in df_death_pivot.columns:
    plt.plot(df_death_pivot.index, df_death_pivot[col], marker='o', label=col)
    
plt.xlabel('Year')
plt.ylabel('Death Count')
plt.title('Yearly Crash Death Count per Unit Type')
plt.legend(title='Unit Type')
plt.grid(True)
plt.show
# %%
# From 2019 to 2020 there were less motor vehicle crashes, probably due to less motor vehicles on the road due to the pandemic
# However from 2019 to 2020 death in motor vehicles remained the same
# Furthermore from 2021 to 2022 there was an increase in moto vehicle crashes, but a decrease in deaths cause by this type of crashes
# Ultimately, we cannot say that less or more motor vehicle crashes equals less or more deaths
# 2 motorized conveyance deaths in the 7 years, we can remove this type
# %%
#merging deaths to total crashes df to further compare
crash_unit_summary = pd.merge(yearly_type_counts, death_yearly_type_counts, how= 'left', on= ['Year', 'Unit Description'])
# %%
#what percent of crashes resulted in deaths for each unit type?
crash_unit_summary['Percent Deaths'] = ((crash_unit_summary['Death Count'] / crash_unit_summary['Crash Count']) * 100).round(1)
# %%
crash_unit_summary
# %%
df_percent_death_pivot = crash_unit_summary.pivot_table(values='Percent Deaths', index=crash_unit_summary.index, columns='Unit Description')
df_percent_death_pivot
# %%
crash_unit_summary.reset_index(inplace=True)
# %%
#making years to a list to use in the plot as x axis
years = crash_unit_summary['Year'].drop_duplicates()
years = years.to_list()
years
# %%
motor_data = crash_unit_summary[crash_unit_summary['Unit Description'] == 'MOTOR VEHICLE']
motor_data
# %%
pedal_data = crash_unit_summary[crash_unit_summary['Unit Description'] == 'PEDALCYCLIST']
pedal_data
# %%
walking_data = crash_unit_summary[crash_unit_summary['Unit Description'] == 'PEDESTRIAN']
walking_data
#%%
#grouping and counting unique type crashes every year, renaming column and making year the index
yearly_type_counts = df.groupby(['Year','Unit Description'])['Crash ID'].nunique().reset_index()
yearly_type_counts.rename(columns={'Crash ID': 'Crash Count'}, inplace=True)
yearly_type_counts.set_index('Year', inplace=True)
yearly_type_counts
#%%
#pivoting so i can trend each unit type
df_pivot = yearly_type_counts.pivot_table(values='Crash Count', index=yearly_type_counts.index, columns='Unit Description')
#%%
#quick plot without customization
df_pivot.plot()
# %%

#%%
#filtering data to only include deaths
filtered_df = df[df['Crash Death Count'] > 0]
#%%
#grouping deathly crashes by unit type, renaming column, and setting year as index
death_yearly_type_counts = filtered_df.groupby(['Year','Unit Description'])['Crash ID'].nunique().reset_index()
death_yearly_type_counts.rename(columns={'Crash ID': 'Death Count'}, inplace=True)
death_yearly_type_counts.set_index('Year', inplace=True)
#%%
motor = motor_data['Crash Count']
motor_death = motor_data['Death Count']
pedal = pedal_data['Crash Count']
pedal_death = pedal_data['Death Count']
walking = walking_data['Crash Count']
walking_death = walking_data['Death Count']
# %%
#creating a bar graph to see how many crashes end in death
yearly_crash_summary = df.groupby(['Year'])['Crash ID'].nunique().reset_index()
yearly_crash_summary.rename(columns={'Crash ID': 'Crash Count'}, inplace=True)
yearly_crash_summary.set_index('Year', inplace=True)
yearly_crash_summary
# %%
#total deaths cause by crashes
yearly_deaths = filtered_df.groupby(['Year'])['Crash ID'].count().reset_index()
#count of crashes that ended in death
yearly_death_summary = filtered_df.groupby(['Year'])['Crash ID'].nunique().reset_index()
yearly_death_summary.set_index('Year', inplace=True)
# %%

#%%
yearly_death_summary
# %%
yearly_death_summary.rename(columns={'Crash ID': 'Deadly Accidents'}, inplace=True)
yearly_deaths.rename(columns={'Crash ID': 'Deaths'}, inplace=True)
# %%
year_summary = pd.merge(yearly_crash_summary, yearly_death_summary, how= 'left', on= ['Year'])
# %%
year_summary = pd.merge(year_summary, yearly_deaths, how= 'left', on= ['Year'])
#%%
year_summary
#%%
import plotly.graph_objects as go

# Sample data

crashes =year_summary['Crash Count']
deaths = year_summary['Deaths']
deadly= year_summary['Deadly Accidents']

# Create traces
trace1 = go.Bar(
    x=years,
    y=crashes,
    name='Crashes'
)
trace2 = go.Bar(
    x=years,
    y=deadly,
    name='Deadly Crashes'
)

# Create the layout
layout = go.Layout(
    barmode='stack',
    title='Yearly Crashes and Deadly Crashes',
    xaxis=dict(title='Crash Year'),
    yaxis=dict(title='Count')
     , width=800, height=400
    
)

# Create the figure
fig = go.Figure(data=[trace2, trace1], layout=layout)

#use log scale to better view death trend
fig.update_layout(xaxis_type="log", yaxis_type="log") 
# Show the figure
fig.show()
# %%
# %%
#vizualizing Walking crashes that end in death
x = years

plt.bar(x, crashes, 0.4 , color = 'y', edgecolor = 'black',
        label='Crashes', bottom=deadly, log=
        True) 

plt.bar(x, deadly, 0.4  , color = 'r', edgecolor = 'black',
        label='Deadly Crashes', log=True) 

plt.xlabel("Crash Year") 
plt.ylabel("Counts") 
plt.title("Yearly Deaths and Crashes")  
plt.legend() 
# %%

# %%

# %%
