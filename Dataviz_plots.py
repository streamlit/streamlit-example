import pandas as pd
import numpy as np 
from   matplotlib import style
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

"""4.1 Visualisation of Accident severity trends across different years

Could see that death rate in accidents is slightly getting reduced over years
Number of accidents also show a reducing trend over years"""

# Extract data for visualisation
df1               = pd.DataFrame(columns=['AccidentId', 'AccidentSeverity', 'Year'])
df1['AccidentId'] = df['AccidentId']
df1['Year']       = df['Year']
df1['AccidentSeverity'] = df['AccidentSeverity'].astype(str)
df1['AccidentSeverity'] = df1['AccidentSeverity']. replace(['1','2','3','4'], ['Not Injured','Died','Injured&Hospitalised','Slightly Injured'])

# Visualise extracted data

crosstb = pd.crosstab(df1['Year'], df1['AccidentSeverity'])
bars = crosstb.plot.bar(width=0.9, color=['red','orange','green','cyan'], stacked=True, figsize=(10,5), ylabel='Accidents', title='Accident Severity over years')

st.pyplot(bars)

"""4.2 Visualisation of Number of Accidents occured over years

The number of accidents reported show a downward trend over years"""

# Extract data for visualisation
df2 = pd.DataFrame()
df2 = df.groupby(['Year'])['Year'].agg(NrOfAccidents=('count')).reset_index()
years = [2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]
# Visualise extracted data
plt.plot(df2['Year'], df2['NrOfAccidents'],color='red', marker='o', linestyle='dashed',linewidth=2, markersize=12)
plt.title('Accidents reported over years')
plt.xlabel('Year')
plt.ylabel('Nr of Accidents')

"""4.3 Analyse if any specific day of the week is more prone to accidents

Could see that Friday is more prone to accidents while Sunday is the day with least number of accidents"""

# Extract data for visualisation
from datetime import datetime
df3 = pd.DataFrame(columns=['AccidentDate','AccidentDay','AccidentDayNr'])
df3['AccidentDate'] = pd.to_datetime(df['AccidentDate'], format='%Y-%m-%d')
df3['AccidentDay']  = df3['AccidentDate'].dt.strftime('%A')
df3['AccidentDayNr']  = df3['AccidentDate'].dt.weekday
df3 = df3.groupby(['AccidentDay','AccidentDayNr'])['AccidentDay'].agg(NrOfAccidents=('count')).reset_index()
df3 = df3.sort_values(['AccidentDayNr'])
df3.head(10)

# Visualise extracted data
df3.plot(x='AccidentDay', y='NrOfAccidents', title='Accident happened in day of week' , style = ["b-*"])
plt.xticks(rotation=90)
plt.ylabel('Nr Of Accidents')


"""4.4 Impact of LightingCondition on Accidents

It looks lighting does not have an impact on the number of accidents as most of the accidents happened during day time."""

# Extract data for visualisation
df4 = pd.DataFrame(columns=['LightingCondition','AccidentSeverity'])
df4 = df.groupby(['LightingCondition','AccidentSeverity'])['LightingCondition'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
lightingLabels = ['Day Time','Dawn/Dusk','Night without public lights','Night with publc lights off',
                  'Night with public light on']
df4['LightingCondition'] = df4['LightingCondition']. replace([1,2,3,4,5], lightingLabels)
df4['AccidentSeverity'] = df4['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='LightingCondition', y='NrOfAccidents', data=df4, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of lighting on Road Accidents')
plt.show()

"""4.5 Impact of AtmosphericCondition on Accidents

It looks like there is no impact of atmospheric condition on accidents. This is because majority of the accidents happened during normal atmospheric condition."""

# Extract data for visualisation
df5 = pd.DataFrame(columns=['AtmosphericCondition','AccidentSeverity'])
df5 = df.groupby(['AtmosphericCondition','AccidentSeverity'])['AtmosphericCondition'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
atmosphericLabels = ['Not Filled','Normal','Light Rain','Heavy Rain','Snow','Fog','Strong Wind','Dazzling Time','Overcast Weather','Other']
df5['AtmosphericCondition'] = df5['AtmosphericCondition']. replace([-1,1,2,3,4,5,6,7,8,9], atmosphericLabels)
df5['AccidentSeverity'] = df5['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='AtmosphericCondition', y='NrOfAccidents', data=df5, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of Atmospheric Condition on Road Accidents')
plt.show()

"""4.6 Impact of Road Category on Accidents

Communal Roads are more prone to accidents and then comes the Departmental Roads"""

# Extract data for visualisation
df6 = pd.DataFrame(columns=['RoadCategory','AccidentSeverity'])
df6 = df.groupby(['RoadCategory','AccidentSeverity'])['RoadCategory'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
roadCategoryLabels = ['Motorway','National Road','Departmental Road','Communal Road','Outside the public network','Car park open to publc traffic','Urban Metropolis Routes','Other']
df6['RoadCategory'] = df6['RoadCategory']. replace([1,2,3,4,5,6,7,9], roadCategoryLabels)
df6['AccidentSeverity'] = df5['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='RoadCategory', y='NrOfAccidents', data=df6, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of RoadCategory on Accidents')
plt.show()

"""4.7 Impact of Intersection Type on Accidents

Among the intersection types 'Out of the intersection', 'X-intersection' and 'T-junction' are more prone to accidents."""

# Extract data for visualisation
df7 = pd.DataFrame(columns=['IntersectionType','AccidentSeverity'])
df7 = df.groupby(['IntersectionType','AccidentSeverity'])['IntersectionType'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
intersectionLabels = ['Out of intersection','X-intersection','T-Junction','Y intersection','Intersection with more than 4 branches','Roundabout','Square','Level Crossing','Other intersection']
df7['IntersectionType'] = df7['IntersectionType']. replace([1,2,3,4,5,6,7,8,9], intersectionLabels)
df7['AccidentSeverity'] = df7['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='IntersectionType', y='NrOfAccidents', data=df7, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of IntersectionType on Accidents')
plt.show()

"""4.8 Impact of Accident Time on Accident severity

It looks like 16:00 PM till 20:00 PM is the most accident prone time.
Also morning till 7:00 AM , the number of accidents are very less"""

# Extract data for visualisation
df8 = pd.DataFrame(columns=['AccidentTimeCategory','AccidentSeverity'])
df8 = df.groupby(['AccidentTimeCategory','AccidentSeverity'])['AccidentTimeCategory'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
timeLabels = ['Till 7AM','7AM-12PM','12PM-16PM','16PM-20PM','20PM-24PM']
df8['AccidentTimeCategory'] = df8['AccidentTimeCategory']. replace([1,2,3,4,5], timeLabels)
df8['AccidentSeverity'] = df8['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='AccidentTimeCategory', y='NrOfAccidents', data=df8, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of Accident time on Severity')
plt.show()

"""4.9 Impact of Area Zone on Accident severity

It looks areazone = 2 ( in built up areas ) is more prone to accidents"""

# Extract data for visualisation
df9 = pd.DataFrame(columns=['AreaZone','AccidentSeverity'])
df9 = df.groupby(['AreaZone','AccidentSeverity'])['AreaZone'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
zoneLabels = ['Outside agglomeration','In built up areas']
df9['AreaZone'] = df9['AreaZone']. replace([1,2], zoneLabels)
df8['AccidentSeverity'] = df8['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='AreaZone', y='NrOfAccidents', data=df9, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of AreaZone on Severity')
plt.show()

"""4.10 Impact of Type of Collision on Accident severity

Other collsion type has the most fatality"""

# Extract data for visualisation
df10 = pd.DataFrame(columns=['CollisionType','AccidentSeverity'])
df10 = df.groupby(['CollisionType','AccidentSeverity'])['CollisionType'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
collisionLabels = ['Two vehicles frontal','Two vehicles from behind','Two vehicles from the side','Three or more vehicles in a chain','Multiple collision','Other collision','Collision free']
df10['CollisionType'] = df10['CollisionType']. replace([1,2,3,4,5,6,7], collisionLabels)
df10['AccidentSeverity'] = df10['AccidentSeverity']. replace([1,2,3,4], severityLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='CollisionType', y='NrOfAccidents', data=df10, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of CollisionType on Severity')
plt.show()

"""4.11 Impact of SurfaceCondition on Accident severity

Most of the accidents happened in normal surface condition"""

# Extract data for visualisation
df11 = pd.DataFrame(columns=['SurfaceCondition','AccidentSeverity'])
df11 = df.groupby(['SurfaceCondition','AccidentSeverity'])['SurfaceCondition'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
surfaceLabels = ['Normal','Wet','Puddles','Flooded','Snowy','Mud','Icy','Fatty substance like oil','Others']
df11['AccidentSeverity'] = df11['AccidentSeverity']. replace([1,2,3,4], severityLabels)
df11['SurfaceCondition'] = df11['SurfaceCondition']. replace([1,2,3,4,5,6,7,8,9], surfaceLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='SurfaceCondition', y='NrOfAccidents', data=df11, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of SurfaceCondition on Severity')
plt.show()

"""4.12 Impact of AccidentSituation on Accident severity

Most of the accidents happened in road"""
# Extract data for visualisation
df12 = pd.DataFrame(columns=['AccidentSituation','AccidentSeverity'])
df12 = df.groupby(['AccidentSituation','AccidentSeverity'])['AccidentSituation'].agg(NrOfAccidents=('count')).reset_index()
severityLabels = ['Not Injured', 'Died','Injured and Hospitalised', 'Slightly Injured']
situationLabels = ['None','On the road','On hard shoulder','On shoulder','On sidewalk','On a cycle path','On another special lane','Others']
df12['AccidentSeverity'] = df12['AccidentSeverity']. replace([1,2,3,4], severityLabels)
df12['AccidentSituation'] = df12['AccidentSituation']. replace([0,1,2,3,4,5,6,8], situationLabels)

# Visualise extracted data
plt.rcParams["figure.figsize"] = [13, 5.50]
plt.rcParams["figure.autolayout"] = True
bar_plot = sns.barplot(x='AccidentSituation', y='NrOfAccidents', data=df12, hue='AccidentSeverity')
plt.xticks(rotation=45)
plt.title('Impact of AccidentSituation on Severity')
plt.show()



