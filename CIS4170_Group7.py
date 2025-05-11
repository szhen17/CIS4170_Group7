#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df=pd.read_csv('Air_Traffic_Passenger_Statistics.csv')
df.head()


# In[3]:


custom={'Domestic':'royalblue','International':'darkorange'}


# In[4]:


# Rename for clarity
df.rename(columns={
    'Operating Airline': 'Airline',
    'GEO Summary': 'Flight Type',
    'Passenger Count': 'Passengers'
}, inplace=True)

# Drop missing values
df2 = df.dropna(subset=['Airline', 'Flight Type', 'Passengers'], inplace=False)

# Step 1: Get total passengers per airline
total_by_airline = df2.groupby('Airline')['Passengers'].sum().reset_index()

# Step 2: Top 10 airlines by total passengers
top_airlines = total_by_airline.sort_values('Passengers', ascending=False).head(10)['Airline'].tolist()

# Step 3: Filter and group by Airline and Flight Type
top_df = df2[df2['Airline'].isin(top_airlines)]
summary = top_df.groupby(['Airline', 'Flight Type'])['Passengers'].sum().reset_index()

# Sort airlines in order of total passengers
airline_order = summary.groupby('Airline')['Passengers'].sum().sort_values(ascending=False).index

# Plot with Seaborn
plt.figure(figsize=(12, 6))
sns.barplot(
    data=summary,
    x='Airline',
    y='Passengers',
    hue='Flight Type',
    order=airline_order,
    palette=custom
)
plt.title('Top 10 Airlines: Domestic vs International Passengers')
plt.xlabel('Airline')
plt.ylabel('Total Passengers')
wrapped_labels = [textwrap.fill(label, width=10) for label in top_airlines]
plt.xticks(ticks=range(0,10,1),labels=wrapped_labels)
plt.legend(title='Flight Type')

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()



# In[5]:


# Drop missing values in key fields
df3 = df.dropna(subset=['Airline', 'Flight Type'])

# Step 1: Count number of flights (i.e., number of records per airline + flight type)
flight_counts = df3.groupby(['Airline', 'Flight Type']).size().reset_index(name='Flight Count')

# Step 2: Get total flights per airline and select top 10
top_airlines = (
    flight_counts.groupby('Airline')['Flight Count']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

# Step 3: Filter to top airlines
top_flight_counts = flight_counts[flight_counts['Airline'].isin(top_airlines)]

# Sort airlines for consistent display
airline_order = (
    top_flight_counts.groupby('Airline')['Flight Count']
    .sum()
    .sort_values(ascending=False)
    .index
)

#plot
plt.figure(figsize=(12, 6))
sns.barplot(
    data=top_flight_counts,
    x='Airline',
    y='Flight Count',
    hue='Flight Type',
    order=airline_order,
    palette=custom
)
#customize
plt.title('Top 10 Airlines: Domestic vs International Flights')
plt.xlabel('Airline')
plt.ylabel('Flight Count')
wrapped_labels = [textwrap.fill(label, width=10) for label in top_airlines]
plt.xticks(ticks=range(0,10,1),labels=wrapped_labels)
plt.legend(title='Flight Type')

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()

