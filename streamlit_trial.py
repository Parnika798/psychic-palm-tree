# -*- coding: utf-8 -*-
"""Streamlit trial.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mmtSSZQeV9PDgqJ1t9u7J1mmKbmurlZq
"""




# Commented out IPython magic to ensure Python compatibility.
# # In a Colab cell
# %%writefile app.py
# import streamlit as st
# 
# st.title("Electoral Insights")
# st.write("A study of Turnout and Advertising Strategies in India's Elections")
# 
# 
#

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# ADVERTISER'S DATASET
advtdf = pd.read_csv('https://github.com/Parnika798/psychic-palm-tree/blob/main/advertisers.csv')
st.write("Advertiser's Dataset", advtdf)

# Replacing ≤100 with 100 to prevent underestimation.
advtdf['Amount spent (INR)'] = advtdf['Amount spent (INR)'].replace('≤100', 100)
st.write("Updated Advertiser's Dataset", advtdf)

advtdf_isnull = advtdf.isnull().sum()
st.write("Missing Values in Advertiser's Dataset", advtdf_isnull)

# LOCATION'S DATASET
locdf = pd.read_csv('/content/locations.csv')
st.write("Location's Dataset", locdf)

locdf_isnull = locdf.isnull().sum()
st.write("Missing Values in Location's Dataset", locdf_isnull)

# RESULTS DATASET
resultsdf = pd.read_csv('/content/results.csv')
st.write("Results Dataset", resultsdf)

# Cleaning the Results dataset: Replace NaN values in 'Phase' column
resultsdf['Phase'].fillna(7.0, inplace=True)
st.write("Updated Results Dataset", resultsdf)

# Drop NaN values in 'State' column
resultsdf.dropna(subset=['State'], inplace=True)

# Find the state with the lowest number of electors
lowestelectors_index = resultsdf['Total Electors'].idxmin()
state_lowestelectors = resultsdf.loc[lowestelectors_index, 'State']
st.write("State with the Lowest Electors", state_lowestelectors)

# MERGING THE DATASETS FOR ANALYSIS
locdf['Location name'] = locdf['Location name'].str.strip().str.lower()
resultsdf['State'] = resultsdf['State'].str.strip().str.lower()
merged = pd.merge(locdf, resultsdf, left_on='Location name', right_on='State', how='inner')

st.write("Merged Dataset", merged)

# DATA VISUALISATION AND ANALYSIS

# Ad Spend vs. Total Votes
st.subheader('Ad Spend vs. Total Votes')
sns.scatterplot(y='Total Votes', x='Amount spent (INR)', data=merged, color='orange')
plt.ylabel('Total votes cast')
plt.xlabel('Total amount spent on advertising in INR')
plt.title('Ad Spend vs. Total Votes', fontsize=25, fontweight='bold')
st.pyplot(plt)

# Ad Spend vs. Voter Turnout
st.subheader('Ad Spend vs. Voter Turnout')
sns.scatterplot(x='Amount spent (INR)', y='Polled (%)', data=merged, color='blue')
plt.title('Ad Spend vs. Voter Turnout', fontsize=25, fontweight='bold')
plt.xlabel('Total amount spent on advertising in INR')
plt.ylabel('Percentage of votes polled')
st.pyplot(plt)

# State vs. Ad Spend
st.subheader('State vs. Ad Spend')
plt.figure(figsize=(12, 8))
plt.grid(True, zorder=1)
sns.barplot(x='State', y='Amount spent (INR)', data=merged, palette=['#E34234', '#2E8B57'], zorder=2)
plt.xlabel('States', fontsize=14, fontweight='bold')
plt.ylabel('Total amount spent on advertising in INR', fontsize=14, fontweight='bold')
plt.title('State vs. Ad Spend', fontsize=25, fontweight='bold')
plt.xticks(rotation=90, ha='center', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# State vs. Voter Turnout
st.subheader('State vs. Voter Turnout')
plt.figure(figsize=(12, 8))
plt.grid(True, zorder=1)
sorted_data = merged.sort_values(by='Polled (%)', ascending=False)
sns.barplot(x='State', y='Polled (%)', data=sorted_data, palette='viridis', zorder=2)
plt.xlabel('States', fontsize=14, fontweight='bold')
plt.ylabel('Percentage of votes polled', fontsize=14, fontweight='bold')
plt.title('State vs. Voter Turnout', fontsize=25, fontweight='bold')
plt.xticks(rotation=90, ha='center', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Phase-wise Ad Spend
st.subheader('Phase-wise Ad Spend')
plt.figure(figsize=(12, 8))
plt.grid(True, zorder=1)
sns.barplot(x='Phase', y='Amount spent (INR)', data=merged, palette='Reds', zorder=2)
plt.xlabel('Phase', fontsize=14, fontweight='bold')
plt.ylabel('Total amount spent on advertising in INR', fontsize=14, fontweight='bold')
plt.title('Phase-wise Ad Spend', fontsize=30, fontweight='bold')
plt.xticks(rotation=90, ha='center', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Assuming 'merged' is already defined and available

# Create the plot
plt.figure(figsize=(12, 8))  # Adjust width and height as needed
plt.grid(True, zorder=1)

# Bar plot
sns.barplot(x='Phase', y='Polled (%)', data=merged, palette='Reds', zorder=2)

# Labels and title
plt.xlabel('Phase', fontsize=14, fontweight='bold')
plt.ylabel('% of Polled Votes', fontsize=14, fontweight='bold')
plt.title('Phase wise Polled (%)', fontsize=30, fontweight='bold')

# Rotate x-axis labels for better readability
plt.xticks(rotation=90, ha='center', fontsize=12)

# Adjust layout for better spacing
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'merged' is already defined and available

# Create the figure and axis
fig, ax1 = plt.subplots(figsize=(14, 8))
plt.grid(True, zorder=1)

# First plot: Total Electors by State (primary y-axis)
sns.barplot(x='State', y='Total Electors', data=merged, ax=ax1, color='lightblue', zorder=2)
ax1.set_xlabel('State', fontsize=14, fontweight='bold')
ax1.set_ylabel('Total Electors', fontsize=14, fontweight='bold', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Rotate x-axis labels
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, ha='center')

# Second plot: Polled (%) by State (secondary y-axis)
ax2 = ax1.twinx()
sns.lineplot(x='State', y='Polled (%)', data=merged, ax=ax2, color='darkgreen', marker='o')
ax2.set_ylabel('Polled (%)', fontsize=14, fontweight='bold', color='darkgreen')
ax2.tick_params(axis='y', labelcolor='darkgreen')

# Title
plt.title('Total Electors and Polled (%) by State', fontsize=25, fontweight='bold')

# Adjust layout
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Assuming 'advtdf' is already defined and available

# Step 1: Convert 'Amount spent (INR)' to numeric and drop NaN values
advtdf['Amount spent (INR)'] = pd.to_numeric(advtdf['Amount spent (INR)'], errors='coerce')
advtdf.dropna(subset=['Amount spent (INR)'], inplace=True)

# Group by 'Page name' and sum the 'Amount spent (INR)'
party_ad_spend = advtdf.groupby('Page name')['Amount spent (INR)'].sum().sort_values(ascending=False)

# Get the top 10 contributors
top_10_parties = party_ad_spend.head(10)

# For better visibility, explode function is being used
explode = [0.05] * len(top_10_parties)  # 0.05 separates each slice by 5% of the radius

# Create the Pie Chart
plt.figure(figsize=(10, 8))
plt.pie(
    top_10_parties,
    labels=top_10_parties.index,
    autopct='%1.1f%%',
    startangle=140,
    explode=explode,  # Applies the exploded effect to each slice
    textprops={'fontsize': 8}
)

plt.title('Top 10 Contributors by Amount Spent on Advertising', fontweight='bold', fontsize=18)

# Ensure the pie is drawn as a circle
plt.axis('equal')

# Display the plot in Streamlit
st.pyplot(plt)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Assuming `merged` is already defined and available in your Streamlit app

# Calculate Voter Turnout percentage
merged['Voter Turnout (%)'] = (merged['Total Votes'] / merged['Total Electors']) * 100

# Selecting relevant columns for correlation analysis
correlation_data = merged[['Amount spent (INR)', 'Total Electors', 'Total Votes', 'Polled (%)', 'Voter Turnout (%)']]

# Calculating the correlation matrix
correlation_matrix = correlation_data.corr()

# Create a heatmap to visualize correlations
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar=True)

# Adding title
plt.title('Correlation Heatmap of Voter Turnout and Ad Spend Metrics')

# Display the plot in Streamlit
st.pyplot(plt)
