import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

import pandas as pd

#Reading the data from the website
url_data = (r'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
df = pd.read_csv(url_data)
#RMD FILE = https://github.com/owid/covid-19-data/blob/master/public/data/README.md



#### DATA CLEANING ####################################################################################################

# 1. Dataframe only for UK
df_UK=df[df["location"]== "United Kingdom"]

df_UK=df_UK.drop(["new_cases_smoothed", "new_deaths_smoothed", "handwashing_facilities",
              "excess_mortality_cumulative_absolute", "excess_mortality_cumulative","excess_mortality",
              "excess_mortality_cumulative_per_million","icu_patients_per_million","hosp_patients_per_million",
              "weekly_icu_admissions_per_million","weekly_hosp_admissions_per_million",'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand','tests_per_case', 'tests_units','new_vaccinations_smoothed','people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million',
       'new_people_vaccinated_smoothed',
       'new_people_vaccinated_smoothed_per_hundred','aged_70_older',"total_cases_per_million",
                    "new_cases_per_million"], axis=1)

df_UK['date'] = pd.to_datetime(df_UK['date'], infer_datetime_format=True)

# 2. Dataframe only for US
df_US=df[df["location"]== "United States"]

df_US=df_US.drop(["new_cases_smoothed", "new_deaths_smoothed", "handwashing_facilities",
              "excess_mortality_cumulative_absolute", "excess_mortality_cumulative","excess_mortality",
              "excess_mortality_cumulative_per_million","icu_patients_per_million","hosp_patients_per_million",
              "weekly_icu_admissions_per_million","weekly_hosp_admissions_per_million",'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand','tests_per_case', 'tests_units','new_vaccinations_smoothed','people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million',
       'new_people_vaccinated_smoothed',
       'new_people_vaccinated_smoothed_per_hundred','aged_70_older',"total_cases_per_million",
                    "new_cases_per_million"], axis=1)

df_US['date'] = pd.to_datetime(df_US['date'], infer_datetime_format=True)

# 3. Dataframe only for Brazil

df_Brazil=df[df["location"]== "Brazil"]

df_Brazil=df_Brazil.drop(["new_cases_smoothed", "new_deaths_smoothed", "handwashing_facilities",
              "excess_mortality_cumulative_absolute", "excess_mortality_cumulative","excess_mortality",
              "excess_mortality_cumulative_per_million","icu_patients_per_million","hosp_patients_per_million",
              "weekly_icu_admissions_per_million","weekly_hosp_admissions_per_million",'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand','tests_per_case', 'tests_units','new_vaccinations_smoothed','people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million',
       'new_people_vaccinated_smoothed',
       'new_people_vaccinated_smoothed_per_hundred','aged_70_older',"total_cases_per_million",
                    "new_cases_per_million"], axis=1)

df_Brazil['date'] = pd.to_datetime(df_Brazil['date'], infer_datetime_format=True)

#4. Dataframe for the whole world
df_world= df.drop(["new_cases_smoothed", "new_deaths_smoothed", "handwashing_facilities",
              "excess_mortality_cumulative_absolute", "excess_mortality_cumulative","excess_mortality",
              "excess_mortality_cumulative_per_million","icu_patients_per_million","hosp_patients_per_million",
              "weekly_icu_admissions_per_million","weekly_hosp_admissions_per_million",'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand','tests_per_case', 'tests_units','new_vaccinations_smoothed',
        'people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million',
       'new_people_vaccinated_smoothed',
       'new_people_vaccinated_smoothed_per_hundred','aged_70_older',"total_cases_per_million",
                    "new_cases_per_million"], axis=1)

df_world['date'] = pd.to_datetime(df_world['date'], infer_datetime_format=True)

df_world= df_world[df_world['location'] !='Africa']
df_world= df_world[df_world['location'] !='Asia']
df_world= df_world[df_world['location'] !='Europe']
df_world= df_world[df_world['location'] !='European Union']
df_world= df_world[df_world['location'] !='Low income']
df_world= df_world[df_world['location'] !='High income']
df_world= df_world[df_world['location'] !='Lower middle income']
df_world= df_world[df_world['location'] !='Oceania']
df_world= df_world[df_world['location'] !='South America']
df_world= df_world[df_world['location'] !='North America']
df_world= df_world[df_world['location'] !='Upper middle income']
df_world= df_world[df_world['location'] !='World']

#5. Dataframe for only the continents
df_continents= df.drop(["new_cases_smoothed", "new_deaths_smoothed", "handwashing_facilities",
              "excess_mortality_cumulative_absolute", "excess_mortality_cumulative","excess_mortality",
              "excess_mortality_cumulative_per_million","icu_patients_per_million","hosp_patients_per_million",
              "weekly_icu_admissions_per_million","weekly_hosp_admissions_per_million",'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand','tests_per_case', 'tests_units','new_vaccinations_smoothed',
       'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'new_vaccinations_smoothed_per_million',
       'new_people_vaccinated_smoothed',
       'new_people_vaccinated_smoothed_per_hundred','aged_70_older',"total_cases_per_million",
                    "new_cases_per_million"], axis=1)

df_continents['date'] = pd.to_datetime(df_continents['date'], infer_datetime_format=True)

continents= ['Africa','Asia','Europe', 'Oceania', 'South America', 'North America' ]
df_continents= df_continents[df_continents['location'].isin(continents)]

#Saving the cleaned data as a csv file
df_US.to_csv('Data\df_US.csv')
df_Brazil.to_csv('Data\df_Brazil.csv')
df_UK.to_csv('Data\df_UK.csv')
df_world.to_csv('Data\df_world.csv')
df_continents.to_csv('Data\df_continents.csv')