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

# 
# 
#

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# First Heading (Electoral Insights)
st.markdown("<h2 style='text-align: left; color: #B51648;'>Electoral Insights:</h2>", unsafe_allow_html=True)

# Second Heading (A Study of Turnout and Advertising Strategies)
st.markdown("<h2 style='text-align: left; color: lightseagreen;'>A Study of Turnout and Advertising Strategies</h2>", unsafe_allow_html=True)


# ADVERTISER'S DATASET
advtdf = pd.read_csv('https://raw.githubusercontent.com/Parnika798/psychic-palm-tree/main/advertisers.csv')
#st.write("Advertiser's Dataset", advtdf)

# Replacing ≤100 with 100 to prevent underestimation.
advtdf['Amount spent (INR)'] = advtdf['Amount spent (INR)'].replace('≤100', 100)
#st.write("Updated Advertiser's Dataset", advtdf)

advtdf_isnull = advtdf.isnull().sum()
#st.write("Missing Values in Advertiser's Dataset", advtdf_isnull)

# LOCATION'S DATASET
locdf = pd.read_csv('https://raw.githubusercontent.com/Parnika798/psychic-palm-tree/main/locations.csv')
#st.write("Location's Dataset", locdf)

locdf_isnull = locdf.isnull().sum()
#st.write("Missing Values in Location's Dataset", locdf_isnull)

# RESULTS DATASET
resultsdf = pd.read_csv('https://raw.githubusercontent.com/Parnika798/psychic-palm-tree/main/results.csv')
#st.write("Results Dataset", resultsdf)

# Cleaning the Results dataset: Replace NaN values in 'Phase' column
resultsdf['Phase'].fillna(7.0, inplace=True)
#st.write("Updated Results Dataset", resultsdf)

# Drop NaN values in 'State' column
resultsdf.dropna(subset=['State'], inplace=True)

# Find the state with the lowest number of electors
lowestelectors_index = resultsdf['Total Electors'].idxmin()
state_lowestelectors = resultsdf.loc[lowestelectors_index, 'State']
#st.write("State with the Lowest Electors", state_lowestelectors)

# MERGING THE DATASETS FOR ANALYSIS
locdf['Location name'] = locdf['Location name'].str.strip().str.lower()
resultsdf['State'] = resultsdf['State'].str.strip().str.lower()
merged = pd.merge(locdf, resultsdf, left_on='Location name', right_on='State', how='inner')

#st.write("Merged Dataset", merged)
st.write("\n\n")
# DATA VISUALISATION AND ANALYSIS
# Create columns with different widths (e.g., first column takes 2/4 width, second takes 1/4, third takes 1/4)
col1, col2 = st.columns([10, 10])  # Adjust the widths as needed


# Ad Spend vs. Total Votes
with col1:
    
    sns.scatterplot(y='Total Votes', x='Amount spent (INR)', data=merged, color='orange')
    plt.ylabel('Total votes cast')
    plt.xlabel('Total amount spent on advertising in INR')
    plt.title('Ad Spend vs. Total Votes', fontsize=25, fontweight='bold')
    st.pyplot(plt)
    plt.clf()




# Ad Spend vs. Voter Turnout
with col2:
    sns.scatterplot(x='Amount spent (INR)', y='Polled (%)', data=merged, color='blue')
    plt.title('Ad Spend vs. Voter Turnout', fontsize=25, fontweight='bold')
    plt.xlabel('Total amount spent on advertising in INR')
    plt.ylabel('Percentage of votes polled')
    st.pyplot(plt)
    plt.clf()

# Ensure 'Amount spent (INR)' is numeric, converting non-numeric values to NaN
advtdf['Amount spent (INR)'] = pd.to_numeric(advtdf['Amount spent (INR)'], errors='coerce')


st.write("\n\n")
# Heading for the dropdown selection
st.markdown("<h2 style='text-align: left; color: #B57F90;'>Election 2024: Key Metrics Overview</h2>", unsafe_allow_html=True)

# Dropdown to select what to view
option = st.selectbox(
    'Select an option to view key Election Metrics:',
    ('Total Amount Spent on Ads in 2024 Elections', 'Total Votes Polled in 2024 Elections')
)

# Display the selected option
if option == 'Total Amount Spent on Ads in 2024 Elections':
    total_amount_spent = advtdf['Amount spent (INR)'].sum()
    st.markdown(f" ₹{total_amount_spent:,.0f}", unsafe_allow_html=True)

elif option == 'Total Votes Polled in 2024 Elections':
    total_votes_polled = merged['Total Votes'].sum()
    st.markdown(f"{total_votes_polled:,.0f}", unsafe_allow_html=True)

st.write("\n\n")
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
plt.clf()



col5, col6= st.columns([6,6])
# State vs. Ad Spend

with col5:
    
   plt.figure(figsize=(12, 8))
   plt.grid(True, zorder=1)
   sns.barplot(x='State', y='Amount spent (INR)', data=merged, palette=['#E34234', '#2E8B57'], zorder=2)
   plt.xlabel('States', fontsize=14, fontweight='bold')
   plt.ylabel('Total amount spent on advertising in INR', fontsize=14, fontweight='bold')
   plt.title('State vs. Ad Spend', fontsize=25, fontweight='bold')
   plt.xticks(rotation=90, ha='center', fontsize=12)
   plt.tight_layout()
   st.pyplot(plt)
   plt.clf()

# State vs. Voter Turnout
with col6:
    
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
   plt.clf()


col3, col4= st.columns([6,6])
# Phase-wise Ad Spend
with col3:
    
    plt.figure(figsize=(12, 8))
    plt.grid(True, zorder=1)
    sns.barplot(x='Phase', y='Amount spent (INR)', data=merged, palette='Reds', zorder=2)
    plt.xlabel('Phase', fontsize=14, fontweight='bold')
    plt.ylabel('Total amount spent on advertising in INR', fontsize=14, fontweight='bold')
    plt.title('Phase-wise Ad Spend', fontsize=30, fontweight='bold')
    plt.xticks(rotation=90, ha='center', fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()



import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Assuming 'merged' is already defined and available
with col4:
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
   plt.clf()


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
plt.clf()




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
plt.title('Correlation Heatmap of Voter Turnout and Ad Spend Metrics', fontsize=25, fontweight= 'bold')

# Display the plot in Streamlit
st.pyplot(plt)
plt.clf()

# Heading for the dropdown selection
st.markdown("<h2 style='text-align: right; color: teal;'>Key Insights</h2>", unsafe_allow_html=True)
#Interactive Summaries Using a Dropdown or Selectbox
summary_choice = st.selectbox('Select a graph to view its summary:', ['Ad Spend vs Total Votes', 'State vs Ad Spend', 'Ad Spend vs Voter Turnout', 'State vs Voter Turnout','Phase-wise Analysis', 'Total Electors and Polled(%) by State', 'Correlation Heatmap of voter turnout and Ad Metrics','Top 10 Contributors by Amount Spent on Advertising'])

if summary_choice == 'Ad Spend vs Total Votes':
    st.write("""
    **Summary for Ad Spend vs. Total Votes:**

    - **Weak Correlation**: The scatter plot shows a weak relationship between ad spending and total votes, indicating that higher advertising budgets do not consistently lead to increased votes.
    - **Concentration of Votes**: Most constituencies have ad spending below 1 crore INR, with total votes generally around 1-1.5 million, regardless of spend level.
    - **High-Spend Outlier**: There is an outlier at around 1.75 crore INR in ad spend, but it does not correlate with a significant increase in votes, further emphasizing the limited impact of ad spending on vote counts.

    
    """)




elif summary_choice == 'State vs Ad Spend':
    st.write("""
    **Summary: State vs Ad Spend**

    - **Odisha**: Highest ad spend at **over 1.75 crore INR**, highlighting it as a key battleground.
    - **Maharashtra** and **Andhra Pradesh**: Significant spending around **1 crore INR** each.
    - Minimal ad spend in **Lakshadweep, Mizoram, Nagaland, Manipur,** and **Meghalaya** due to smaller electorates or secure political bases.
    - **Bihar** and **Uttar Pradesh**: Moderate spending, suggesting reliance on alternative campaign strategies.

    **Key Insights**  
    - **Diverse Strategies**: Higher ad spends are targeted in competitive regions.
    - **Selective Investment**: Lower spending in states with stable political landscapes or smaller electorates.
    """)


elif summary_choice == 'Ad Spend vs Voter Turnout':
    st.write("""
    **Voter Turnout Distribution**

    - **Turnout Range**: Voter turnout spans **40% to 90%** across various ad spend levels.
    - **Weak Correlation**: Increased ad spending does not consistently lead to higher turnout; most constituencies cluster between **60-80% turnout** despite different budgets.

    **Key Insights**  
    - **Ad Spend Limitations**: A weak correlation suggests that ad spending alone may not drive voter participation.
    - **Influential Factors**: Constituencies with low ad spend but high turnout may be influenced by factors like local issues or grassroots efforts.
   """)


elif summary_choice == 'State vs Voter Turnout':
    st.write("""
    **Summary:**
    Lakshadweep has the highest voter turnout, slightly exceeding 80%, while Bihar and Uttrakhand stand at the lowest, around 50 -60%.
    **Key Insights** - Turnout appears generally higher in northeastern and some southern states, suggesting that regional political dynamics, cultural factors, or campaign efforts may play a role in mobilizing voters in these areas.
    """)
elif summary_choice == 'Phase-wise Analysis':
    st.write("""
    **Polling Consistency Across Phases**

    - **Consistent Voter Turnout**: Polled percentage remains steady across phases, despite variations in ad spend. 
    - **Phase 4**: Highest polling at around **70%**.
    - **Phases 3 and 5**: Slightly lower polling percentages, reflecting steady voter engagement.

    **Key Insights**  
    - **Ad Spend vs. Voter Turnout**: Increased ad spend in Phase 5 does not correspond with higher polling, suggesting that ad investment alone may not boost turnout.
    - **Strategic Implications**: Parties may benefit from holistic strategies to drive engagement, particularly in phases with stable turnout levels.
    """)


elif summary_choice == 'Total Electors and Polled(%) by State':
    st.write("""
    **Summary: Elector Counts and Voter Turnout**

    - **High Elector Counts in Rajasthan and Haryana**: Both states exceed **2 million electors**, with **turnout rates between 60% and 70%**.
    - **High Turnout in Smaller Electorates**: Smaller states like **Arunachal Pradesh, Lakshadweep, and Sikkim** exceed **75% voter turnout**.

    **Key Insights**  
    - **Elector Count vs. Turnout**: Larger elector counts do not guarantee higher voter turnout, as seen in states with moderate engagement like Rajasthan and Haryana.
    - **High Turnout in Small States**: Smaller states, such as Nagaland and Manipur, achieve high turnout, suggesting **effective voter mobilization strategies**.
    - **Regional Disparities**: Turnout varies significantly by region, highlighting that **local factors impact voter engagement** beyond population size.
    """)


elif summary_choice == 'Correlation Heatmap of voter turnout and Ad Metrics':
    st.write("""
    **Summary: Correlation Analysis**

    - **Ad Spend vs Voter Turnout**: Weak correlation, indicating that **ad spending does not directly drive voter participation**.
    - **Total Electors vs Total Votes**: Positive correlation of **0.68**, showing a strong link between registered voters and votes cast.
    - **Total Electors vs Polled (%) and Voter Turnout (%)**: Negative correlation, suggesting **lower voter engagement in larger electorates**.

    **Key Insights**  
    - **Ad Spend Ineffectiveness**: Increased advertising does not guarantee higher turnout.
    - **Engagement Challenges**: Larger electorates show lower engagement, indicating the need for tailored mobilization strategies.
    - **Strategic Focus**: Political parties may benefit from re-evaluating ad strategies, focusing on factors that better drive voter turnout.
     """)


else: 
    st.write("""
    **Ad Spending Breakdown**

    - **BJP**: Leads with **42.3%** of ad spending, showing substantial investment.
    - **Ama Chinha Sankha Chinha**: Follows at **24.5%**, with competitive spending.
    - **Indian National Congress**: Invests **23.7%**, close to Ama Chinha Sankha Chinha.

    **Key Insights**  
    - **Dominance of BJP**: BJP’s ad spend is nearly **double** that of Ama Chinha Sankha Chinha, showing its dominance in ad investment.
    - **Relative Spending Gaps**: Combined spending by Ama Chinha Sankha Chinha and Indian National Congress is still less than BJP’s total, underscoring BJP's strong commitment to advertising.
    """)


