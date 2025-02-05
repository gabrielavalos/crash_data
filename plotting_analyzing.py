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
df
#%%
yearly_type_summary =  df.groupby(['Year','Unit Description']).agg(
   # crashed_units = ('Crash ID', 'count'), #counting all units involved in crashes
    unique_crashes = ('Crash ID', 'nunique'), #counting unique crashes
    deadly_crashes = ('Crash ID', lambda x: x[df.loc[x.index, 'Deadly Crash'] == 1].nunique())
).reset_index()
#%%
yearly_type_summary.set_index('Year', inplace=True)
#yearly_type_summary
# %%
#pivoting so i can trend each unit type
df_pivot = yearly_type_summary.pivot_table(values=['unique_crashes', 'deadly_crashes'], index=yearly_type_summary.index, columns='Unit Description')
#%%
#df_pivot
# %%
plt.figure(figsize=(10, 8))
colors = ['r', 'c', 'm']    
for col, i in zip(df_pivot['unique_crashes'].columns, colors):
    plt.plot(df_pivot.index, df_pivot['unique_crashes'][col], marker='o',label=col+ ' CRASHES', color=i)

for col, i in zip(df_pivot['deadly_crashes'].columns, colors):
    plt.plot(df_pivot.index, df_pivot['deadly_crashes'][col],  linestyle='dashed', label='DEADLY '+col+' CRASHES', color=i)

plt.xlabel('Year')
plt.ylabel('Crash Count')
plt.yscale('log')
plt.title('Yearly - Crash and Deadly Crash')
plt.legend(title='Unit Type', loc='upper left', bbox_to_anchor=(1,1))
plt.grid(True)
plt.show
# %%
# From 2019 to 2020 there were less motor vehicle crashes, probably due to less motor vehicles on the road due to the pandemic
# However from 2019 to 2020 death in motor vehicles remained the same
# Furthermore from 2021 to 2022 there was an increase in moto vehicle crashes, but a decrease in deaths cause by this type of crashes
# Ultimately, we cannot say that less or more motor vehicle crashes equals less or more deaths
# 2 motorized conveyance deaths in the 7 years, we can remove this type
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
#year_summary
#%%
unit_summary =  df.groupby(['Unit Description']).agg(
   # crashed_units = ('Crash ID', 'count'), #counting all units involved in crashes
    unique_crashes = ('Crash ID', 'nunique'), #counting unique crashes
    deadly_crashes = ('Crash ID', lambda x: x[df.loc[x.index, 'Deadly Crash'] == 1].nunique())
).reset_index()
# %%
unit_summary['deadly_percent'] = ((unit_summary['deadly_crashes'] / unit_summary['unique_crashes'])*100).round(1)
# %%
# crashes = unit_summary['unique_crashes']
# deadly=  unit_summary['deadly_crashes']
unit_type =  unit_summary['Unit Description']
percent = unit_summary['deadly_percent']

# horizontal bar chart
plt.barh(unit_type, percent , color='skyblue')

# Add title and labels
plt.title('Percent of Crashes that are Deadly')
plt.xlabel('Percentage')
plt.ylabel('Unit Type')

# Show the plot
plt.show()
#%%
#crash percent change every year
year_summary['crashes_pchange'] = (year_summary['unique_crashes'].pct_change() * 100).round(0)
year_summary['deadly_pchange'] = (year_summary['deadly_crashes'].pct_change() * 100).round(0)
# %%
# Create traces
trace1 = go.Line(
    x=years,
    y=year_summary['unique_crashes'],
    hovertemplate = '%{y}'+'<br>'+'%{text}',
    #percent change to tooltip
                           text = ['percent change {}'.format(i) for i in year_summary['crashes_pchange']]
, name = 'Crashes'
)

# Create the layout
layout = go.Layout(
    
    title='Yearly Crashes',
    xaxis=dict(title='Crash Year'),
    yaxis=dict(title='Count')
     , width=800, height=400
)
# Create the figure
fig = go.Figure(data=[trace1], layout=layout)
#use log scale to better view death trend
#fig.update_layout(xaxis_type="log", yaxis_type="log") 
# Show the figure
fig.show()
# %%
# Create traces

trace2 = go.Line(
    x=years,
    y=year_summary['deadly_crashes'],
    name='Deadly Crashes'
    , line=dict(color="red")
    ,  hovertemplate = '%{y}'+'<br>'+'%{text}',
    #percent change to tooltip
                           text = ['percent change {}'.format(i) for i in year_summary['deadly_pchange']]
)
# Create the layout
layout = go.Layout(
    title='Yearly Deadly Crashes',
    xaxis=dict(title='Crash Year'),
    yaxis=dict(title='Count')
     , width=800, height=400
     
)
# Create the figure
fig = go.Figure(data=[trace2], layout=layout)

# Show the figure
fig.show()
#significant decrease in deadly crashes from 2022 to 2023, what happened?
