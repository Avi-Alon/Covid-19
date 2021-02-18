# Assignment4 - Final Project

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# use the 'seaborn-colorblind' style
plt.style.use('seaborn-colorblind')

df_covid = pd.read_csv('WHO COVID-19  January 20th 2021.csv')
df_covid = df_covid.iloc[1:]
df_covid = df_covid[['Name', 'Deaths - cumulative total per 1 million population']]
df_covid.rename(columns={'Name': 'Country Name'}, inplace=True)

# Now we have to rename some countries by building a dictionary
Dict_update_country = {'United States of America': 'United States', 'Bolivia (Plurinational State of)': 'Bolivia',
                       'Cabo Verde': 'Cape Verde', "Côte d’Ivoire": "Cote d'Ivoire",
                       'Democratic Republic of the Congo': 'Congo, Dem. Rep.', 'Congo': 'Congo, Rep.',
                       'Czechia': 'Czech Republic', 'Iran (Islamic Republic of)': 'Iran',
                       'Kyrgyzstan': 'Kyrgyz Republic', "Lao People's Democratic Republic": "Lao",
                       'Republic of Moldova': 'Moldova', "Democratic People's Republic of Korea": "North Korea",
                       "Republic of Korea": "South Korea", "Russian Federation": "Russia",
                       "Slovakia": "Slovak Republic", "South Sudan": "Sudan", "Syrian Arab Republic": "Syria",
                       "The United Kingdom": "United Kingdom", "United Republic of Tanzania": "Tanzania",
                       "Venezuela (Bolivarian Republic of)": "Venezuela", "Viet Nam": "Vietnam",
                       "occupied Palestinian territory, including east Jerusalem": "Palestine"}
df_covid['Country Name'] = df_covid['Country Name'].replace(Dict_update_country)
df_covid = df_covid.sort_values('Country Name').set_index('Country Name')
#print("df_covid shape: ", df_covid.shape)
#print('-------------------------------------------------')

# Now we open the "Democracy index" excel (xlsx) file
df_democ_ind = pd.read_excel("Democracy Indices.xlsx", engine='openpyxl', sheet_name='data-for-countries-etc-by-year')
# Let's use mask to select data only from 2019
only_2019_mask = df_democ_ind['time'] == 2019
df_democ_ind_19 = df_democ_ind.where(only_2019_mask).dropna()

# Now let's reduce the dataframe to the required columns
df_democ_ind_19 = df_democ_ind_19[['name', 'Democracy index (EIU)']]
df_democ_ind_19.rename(columns={'name': 'Country Name', 'Democracy index (EIU)': 'Democracy index'}, inplace=True)
df_democ_ind_19 = df_democ_ind_19.set_index('Country Name')
#print("df_democ_ind_19 shape: ", df_democ_ind_19.shape)
#print('-------------------------------------------------')

# Now we are ready to merge
merged_pd = pd.merge(df_democ_ind_19, df_covid, how='inner', left_index=True, right_index=True)
print(merged_pd.head())
print('-------------------------------------------------')

# Now we can covert "Democracy index" and "Deaths - cumulative total per 1 million population" columns
# into lists in order to compute correlation
corr = stats.pearsonr(merged_pd['Democracy index'].tolist(),
                      merged_pd['Deaths - cumulative total per 1 million population'].tolist())
print("The correlation is: ", corr[0])
print("The P value is: ", corr[1])

# # Finally, we will produce some visualizations of the results
# plt.plot(merged_pd['Democracy index'].tolist(),
#                      merged_pd['Deaths - cumulative total per 1 million population'].tolist(), 'o')
#plt.show()

# Due to seaborn, we can also make figure strait from dataframe
merged_pd.plot('Democracy index', 'Deaths - cumulative total per 1 million population', kind = 'scatter')
plt.title('Positive correlation between Covid-19 Death Rate and democracy index', fontsize=16)
# Now we will emphasise some special dots
plt.plot(merged_pd.loc['Israel', 'Democracy index'],
         merged_pd.loc['Israel', 'Deaths - cumulative total per 1 million population'],
         color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=12)
plt.text(merged_pd.loc['Israel', 'Democracy index'],
         merged_pd.loc['Israel', 'Deaths - cumulative total per 1 million population'],
         s='Israel', fontsize=12)
plt.plot(merged_pd.loc['United States', 'Democracy index'],
         merged_pd.loc['United States', 'Deaths - cumulative total per 1 million population'],
         color='red', marker='o', linestyle='dashed', linewidth=2, markersize=12)
plt.text(merged_pd.loc['United States', 'Democracy index'],
         merged_pd.loc['United States', 'Deaths - cumulative total per 1 million population'],
         s='United States', fontsize=12)
plt.plot(merged_pd.loc['Sweden', 'Democracy index'],
         merged_pd.loc['Sweden', 'Deaths - cumulative total per 1 million population'],
         color='yellow', marker='o', linestyle='dashed', linewidth=2, markersize=12)
plt.text(merged_pd.loc['Sweden', 'Democracy index'],
         merged_pd.loc['Sweden', 'Deaths - cumulative total per 1 million population'],
         s='Sweden', fontsize=12)

plt.show()


