# Importing packages
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

# Main titles and description
st.title('COVID-19 Dashboard')
st.markdown('This Dashboard displays the worldwide cases and deaths of Covid-19 over time. It is based on the data by Our World in Data. This includes the information about positive cases, deaths and vaccinations per country.')

# Data Caching
@st.cache
def get_data(url):
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df.date).dt.date
    df['date'] = pd.DatetimeIndex(df.date)
    return df

# Loading the data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = get_data(url)

locations = df.location.unique().tolist()

# Removing Continents and other unwanted categories from the country selection list
locations_to_remove = ['Africa', 'Asia', 'Australia', 'Europe', 'European Union', 'High income', 'International', 'Low income', 'Lower middle income', 'Oceania', 'South America', 'Upper middle income', 'World']
for loc in locations_to_remove:
    locations.remove(loc)

# Defining sidebar and titles
sidebar = st.sidebar
sidebar.title("Category Filter")
sidebar.markdown("Please choose your options for data display")

# Date selection
sidebar.markdown("Choose a date")
start_date = sidebar.date_input('Start date', datetime.date(2020, 2, 24))
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
end_date = sidebar.date_input('End date', tomorrow)
if start_date < end_date:
    sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    sidebar.error('Error: End date must fall after start date.')

# Filtering by date
start_date = np.datetime64(start_date)
end_date = np.datetime64(end_date)
df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > start_date) & (df['date'] <= end_date)
df = df.loc[mask]

# Format of numbers: 7day_rolling_avg
df['7day_rolling_avg_cases_per_million'] = df['new_cases_per_million'].rolling(window=7).mean()
df['7day_rolling_avg_deaths_per_million'] = df['new_deaths_per_million'].rolling(window=7).mean()
df['7day_rolling_avg_vaccinations_per_million'] = df['new_vaccinations_smoothed_per_million'].rolling(window=7).mean()

# Format of numbers: cumulative_number
df=df.sort_values(['date']).reset_index(drop=True)
df['new_cases_per_million'] = df['new_cases_per_million'].fillna(0)
df['cumulative_number_cases_per_million'] = df.groupby(['location'])['new_cases_per_million'].cumsum(axis=0)
df['new_deaths_per_million'] = df['new_deaths_per_million'].fillna(0)
df['cumulative_number_deaths_per_million'] = df.groupby(['location'])['new_deaths_per_million'].cumsum(axis=0)
df['new_vaccinations_smoothed_per_million'] = df['new_vaccinations_smoothed_per_million'].fillna(0)
df['cumulative_number_vaccinations_per_million'] = df.groupby(['location'])['new_vaccinations_smoothed_per_million'].cumsum(axis=0)

# Selecting the country
selected = sidebar.multiselect("Choose a location", locations, default=["France"])
st.markdown(f"### Selected countries: {', '.join(selected)}")

# Filtering and grouping by country
trend_data = df.query(f"location in {selected}").\
    groupby(["location", pd.Grouper(key="date", 
    freq="1D")]).aggregate(new_cases=("new_cases_per_million", "sum"),
    new_deaths = ("new_deaths_per_million", "sum"),
    new_vaccinations = ("new_vaccinations_smoothed_per_million", "sum"),
    rolling_avg_cases = ("7day_rolling_avg_cases_per_million", "sum"),
    rolling_avg_deaths = ("7day_rolling_avg_deaths_per_million", "sum"),
    rolling_avg_vaccinations = ("7day_rolling_avg_vaccinations_per_million", "sum"),
    cumulative_number_cases = ("cumulative_number_cases_per_million", "sum"),
    cumulative_number_deaths = ("cumulative_number_deaths_per_million", "sum"),
    cumulative_number_vaccinations = ("cumulative_number_vaccinations_per_million", "sum"),
    ).reset_index()

trend_data["date"] = trend_data.date.dt.date

# Selecting the data type
selected_type1 = sidebar.radio("Choose a data type", ["New Cases", "New Deaths", "New Vaccinations"])
if selected_type1 == "New Cases":
    m = 0
if selected_type1 == "New Deaths":
    m = 1
if selected_type1 == "New Vaccinations":
    m = 2

# Selecting the data format
selected_type2 = sidebar.radio("Choose a data format", ["Raw Number per Million", "7-Day Rolling Average per Million", "Cumulative Number per Million"])
if selected_type2 == "Raw Number per Million":
    n = 0
if selected_type2 == "7-Day Rolling Average per Million":
    n = 1
if selected_type2 == "Cumulative Number per Million":
    n = 2

# Selectin the coluns of the dataframe
mn = 3*n+m
lines = [False for i in range(9)]
lines[mn] = True
line_cols = ["new_cases_per_million", "new_deaths_per_million", "new_vaccinations_smoothed_per_million", "rolling_average_cases_per_million", "rolling_average_deaths_per_million", "rolling_average_vaccinations_per_million", "cumulative_number_cases_per_million", "cumulative_number_deaths_per_million", "cumulative_number_vaccinations_per_million"]
trends = [c[1] for c in zip(lines,line_cols) if c[0]==True]

ndf = pd.DataFrame(data=trend_data.date.unique(),columns=["date"])

# Selecting the countries
for s in selected:
    new_cols = ["date"]+[f"{s}_{c}" for c in line_cols]
    tdf = trend_data.query(f"location=='{s}'")
    tdf.drop("location", axis=1, inplace=True)
    tdf.columns=new_cols
    ndf=ndf.merge(tdf,on="date",how="inner")
    
# List of the trends to plot
new_trends = []
for c in trends:
    new_trends.extend([f"{s}_{c}" for s in selected])

# Ploting the trends
if len(trends)>0:
    
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    for _ in range(0,len(new_trends)):
        ax.plot(ndf["date"],ndf[new_trends[_]], label=new_trends[_])
    
    ax.set_xlabel("Date")
    ax.set_ylabel(selected_type1+'  —  '+selected_type2)
    ax.xaxis.grid(True, linestyle='--')
    ax.yaxis.grid(True, linestyle='--')
    ax.legend(loc="upper left")
    fig.subplots_adjust(left=0,bottom=0,right=1,top=0.92,wspace=0,hspace=0)
    st.plotly_chart(fig, use_container_width=False)

# Extraction of Peaks
if selected_type2 == "Cumulative Number per Million":
    sidebar.markdown("Choose to find the peak of cumulative")
    peak_on_off = sidebar.checkbox("Find Peak")

    if peak_on_off == True:
        st.markdown(f"### Peak values based on cummulative number:")

        for _ in range(0,len(selected)):
            deriv_ndf = ( ndf[new_trends[_]] - ndf[new_trends[_]].shift(1) ) / 1
            max_val = np.max(deriv_ndf)
            date_max_val = ndf["date"][np.argmax(deriv_ndf)]
            st.markdown("Peak value for **"+selected[_]+"** and **"+selected_type1+"**: **"+str(round(max_val,2))+"**, on date: **"+str(date_max_val)+"**")
