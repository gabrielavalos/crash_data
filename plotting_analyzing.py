#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# %%
df = pd.read_csv('C:/Users/Ville/OneDrive/Desktop/crash_data/cleanned_transformed.csv')
# %%
#creating a binary column if there were more than 0 deaths
df['Deadly Crash'] = np.where(df['Crash Death Count'] > 0, 1,0)
# %%
#df
#%%
#df_pivot
#%%
#making years to a list to use in the plot as x axis
years = df['Year'].drop_duplicates()
years = years.to_list()
#years
# %%
#yearly counts
year_summary =  df.groupby(['Year']).agg(
   # crashed_units = ('Crash ID', 'count'), #counting all units involved in crashes
    unique_crashes = ('Crash ID', 'nunique'), #counting unique crashes
    deadly_crashes = ('Crash ID', lambda x: x[df.loc[x.index, 'Deadly Crash'] == 1].nunique())
).reset_index()
#%%
#crash percent change every year
year_summary['crashes_pchange'] = (year_summary['unique_crashes'].pct_change() * 100).round(0)
year_summary['deadly_pchange'] = (year_summary['deadly_crashes'].pct_change() * 100).round(0)
#%%
c = year_summary['unique_crashes'] 
d = year_summary['deadly_crashes']
# %%
#%%
year_summary['percent_deadly'] = ((year_summary['deadly_crashes'] / year_summary['unique_crashes']) * 100).round(1)
year_summary

#%%
#CRASH AND DEADLY CRASH TRENDS - DOUBLE AXIS
# Create figure with secondary y-axis
fig, ax1 = plt.subplots(figsize=(10,5))
#FIRST AXIS
ax1.bar(years, c, linestyle= '-', color='skyblue', label='Total Crashes')
ax1.set_xlabel('Year')
ax1.set_ylabel("Crash Count")
ax1.tick_params(axis='y')
#TWINING FOR DOUBLE AXIS
ax2 = ax1.twinx()
#2ND AXIS SPECS
ax2.plot(years, year_summary['percent_deadly'], linestyle= '-', marker='o', color='red', label='Deadly %')
ax2.set_xlabel('Year')
ax2.set_ylabel("Percent")
ax2.tick_params(axis='y')

ax1.legend(loc='lower right', bbox_to_anchor=(0.5,-0.25))
ax2.legend(loc='lower right',  bbox_to_anchor=(0.70,-0.25))
#PLOT
plt.title('Yearly Crashes and % Deadly Crashes')
plt.show()
# KEY TAKEAWAY: LESS CRASHES DOES NOT MEAN LESS DEADLY CRASHES
# FROM 2019 TO 2020, TOTAL CRASHES DECRESED, BUT PERCENTAGE OF DEADLY CRASHES INCREASED, 2023 TO 2024 FOLLOWS A SIMILAR TREND
# FROM 2020 TO 2022, TOTAL CRASHES STEADLY INCREASED, BUT PERCENTAGE OF DEADLY CRASHES DID NOT FOLLOW A SIMILAR INCREASE TREND
# FROM 2022 TO 2024, TOTAL CRASHES STEADEALY DECREASED, BUT DEADLY CRASHES SIGNIFICANTLY DECREASED, THEN SIGNIFICANTLY INCREASED
#%%
yearly_type_summary =  df.groupby(['Year','Unit Description']).agg(
   # crashed_units = ('Crash ID', 'count'), #counting all units involved in crashes
    unique_crashes = ('Crash ID', 'nunique'), #counting unique crashes
    deadly_crashes = ('Crash ID', lambda x: x[df.loc[x.index, 'Deadly Crash'] == 1].nunique())
).reset_index()
#%%
yearly_type_summary.set_index('Year', inplace=True)
#%%
#yearly_type_summary
# %%
#pivoting to trend out
df_pivot = yearly_type_summary.pivot_table(values=['unique_crashes', 'deadly_crashes'], index=yearly_type_summary.index, columns='Unit Description')
#%%
#GROUPING BY UNIT AND YEAR
unit_summary =  df.groupby(['Unit Description']).agg(
   # crashed_units = ('Crash ID', 'count'), #counting all units involved in crashes
    unique_crashes = ('Crash ID', 'nunique'), #counting unique crashes
    deadly_crashes = ('Crash ID', lambda x: x[df.loc[x.index, 'Deadly Crash'] == 1].nunique())
).reset_index()
#%%
unit_summary['deadly_percent'] = ((unit_summary['deadly_crashes'] / unit_summary['unique_crashes'])*100).round(1)
#%%
colors = ['orange', 'c', 'm']   
fig, ax1 = plt.subplots(figsize=(10,5))
#FIRST AXIS
for col, i in zip(df_pivot['unique_crashes'].columns, colors):
    ax1.plot(df_pivot.index, df_pivot['unique_crashes'][col], marker='o', color=i, label=col+ ' CRASHES')
ax1.set_xlabel('Year')
ax1.set_ylabel("Crash Count")
ax1.tick_params(axis='y')

#TWINING FOR DOUBLE AXIS
ax2 = ax1.twinx()

#2ND AXIS SPECS
for col, i in zip(df_pivot['deadly_crashes'].columns, colors):
    ax2.plot(df_pivot.index, df_pivot['deadly_crashes'][col],  linestyle='dashed', color=i, label='DEADLY ' + col + ' CRASHES')
ax2.set_xlabel('Year')
ax2.set_ylabel("Percent")
ax2.tick_params(axis='y')

ax1.legend(loc='lower left', bbox_to_anchor=(-.01,-0.35))
ax2.legend(loc='lower right',  bbox_to_anchor=(1,-0.35))
#PLOT
plt.title('Yearly Unit Type Crashes and Deadly Crashes')
plt.show()
# %%
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df_pivot.index, df_pivot['unique_crashes']['PEDESTRIAN'], color='orange', label='Crashes')
ax1.set_xlabel('Year')
ax1.set_ylabel("Crash Count")
ax1.tick_params(axis='y')
ax2 = ax1.twinx()
ax2.plot(df_pivot.index, df_pivot['deadly_crashes']['PEDESTRIAN'], linestyle='dashed', color='orange', label='Deadly Crashes')
ax2.set_xlabel('Year')
ax2.set_ylabel("Crash Count")
ax2.tick_params(axis='y')
ax1.legend(loc='lower left')
ax2.legend(loc='lower right')
plt.title('Pedestrian')
plt.show()
# %%
#MOTOR
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df_pivot.index, df_pivot['unique_crashes']['MOTOR VEHICLE'], color='c', label='MOTOR CRASHES')
ax1.set_xlabel('Year')
ax1.set_ylabel("Crash Count")
ax1.tick_params(axis='y')
ax2 = ax1.twinx()
ax2.plot(df_pivot.index, df_pivot['deadly_crashes']['MOTOR VEHICLE'], linestyle='dashed', color='c', label='MOTOR DEADLY CRASHES')
ax2.set_xlabel('Year')
ax2.set_ylabel("Crash Count")
ax2.tick_params(axis='y')
ax1.legend(loc='lower left')
ax2.legend(loc='lower right')
plt.title('Motor Vehicle')
plt.show()
# %%
#PEDACYCLIST
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df_pivot.index, df_pivot['unique_crashes']['PEDALCYCLIST'], color='m', label='PEDALCYCLIST CRASHES')
ax1.set_xlabel('Year')
ax1.set_ylabel("Crash Count")
ax1.tick_params(axis='y')
ax2 = ax1.twinx()
ax2.plot(df_pivot.index, df_pivot['deadly_crashes']['PEDALCYCLIST'], linestyle='dashed', color='m', label='PEDALCYCLYST DEADLY CRASHES')
ax2.set_xlabel('Year')
ax2.set_ylabel("Crash Count")
ax2.tick_params(axis='y')
ax1.legend(loc='lower left')
ax2.legend(loc='lower right')
plt.title('Pedacyclist')
plt.show()

# %%

#%%
# COMPARING % OF UNIT CRASHES THAT ARE DEADLY
# crashes = unit_summary['unique_crashes']
# deadly=  unit_summary['deadly_crashes']
unit_type =  unit_summary['Unit Description']
percent = unit_summary['deadly_percent']
#PLOTTING
plt.figure(figsize=(10, 8))
plt.barh(unit_type, percent , color='skyblue')
#title and labels
plt.title('Percent of Crashes that are Deadly')
plt.xlabel('Percentage')
plt.ylabel('Unit Type')
# Show the plot
plt.show()
#%%









# %%


# #CRASH AND DEADLY CRASH TRENDS - DOUBLE AXIS
# # Create figure with secondary y-axis
# fig, ax1 = plt.subplots(figsize=(10,5))
# #FIRST AXIS
# ax1.plot(years, c, linestyle= '-', marker='o', color='blue', label='total crashes')
# ax1.set_xlabel('Year')
# ax1.set_ylabel("Crash Count", color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')
# #TWINING FOR DOUBLE AXIS
# ax2 = ax1.twinx()
# #2ND AXIS SPECS
# ax2.plot(years, d, linestyle= '-', marker='o', color='red', label='total deaths')
# ax2.set_xlabel('Year')
# ax2.set_ylabel("Death Count", color='red')
# ax2.tick_params(axis='y', labelcolor='red')

# ax1.legend(loc='upper left')
# ax2.legend(loc='upper right')
# #PLOT
# plt.title('Yearly Crashes and Deadly Crashes')
# plt.show()
# #YEAR UNIT TYPE TRENDS
# plt.figure(figsize=(10, 8))
# colors = ['r', 'c', 'm']    
# #CRASHES
# for col, i in zip(df_pivot['unique_crashes'].columns, colors):
#     plt.plot(df_pivot.index, df_pivot['unique_crashes'][col], marker='o',label=col+ ' CRASHES', color=i)
# #DEADLY CRASHES
# for col, i in zip(df_pivot['deadly_crashes'].columns, colors):
#     plt.plot(df_pivot.index, df_pivot['deadly_crashes'][col],  linestyle='dashed', label='DEADLY '+col+' CRASHES', color=i)
# #PLOT SPECS
# plt.xlabel('Year')
# plt.ylabel('Crash Count')
# plt.yscale('log')
# plt.title('Yearly - Unit Crash and Deadly Crash')
# plt.legend(title='Unit and Crash Type', loc='upper left', bbox_to_anchor=(1,1))
# plt.grid(True)
# plt.show