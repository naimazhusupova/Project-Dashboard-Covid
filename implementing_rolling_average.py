import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cufflinks
import datetime
import seaborn as sns


st.title('COVID-19 Dashboard')
st.markdown('This Dashboard displays the worldwide cases and deaths of Covid-19 over time. It is based on the data by Our World in Data. This includes the information about positive cases, deaths and vaccinations per country.')
st.sidebar.title("Category Filter")
#st.sidebar.markdown("Here we will give further information about our project or implement some cool widgets!")

#Data Caching
@st.cache
def get_data(url):
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df.date).dt.date
    df['date'] = pd.DatetimeIndex(df.date)
    return df

#Loading the data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = get_data(url)

locations = df.location.unique().tolist()

sidebar = st.sidebar


#Date selection
st.sidebar.markdown("Choose a date")
start_date = st.sidebar.date_input('Start date')
end_date = st.sidebar.date_input('End date')
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')


start_date = np.datetime64(start_date)
end_date = np.datetime64(end_date)
df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > start_date) & (df['date'] <= end_date)
df = df.loc[mask]

#Format of numbers
df['7day_rolling_avg_cases'] = df['new_cases'].rolling(window=7).mean()
df['7day_rolling_avg_deaths'] = df['new_deaths'].rolling(window=7).mean()
df['cumulative_number_cases'] = df['new_cases'].cumsum(axis = 0)
df['cumulative_number_deaths'] = df['new_deaths'].cumsum(axis = 0)

selected = sidebar.multiselect("Choose a location", locations)
st.markdown(f"### You Selected: {', '.join(selected)}")

trend_data = df.query(f"location in {selected}").\
    groupby(["location", pd.Grouper(key="date", 
    freq="1D")]).aggregate(new_cases=("new_cases", "sum"),
    new_deaths = ("new_deaths", "sum"),
    new_vaccinations = ("new_vaccinations", "sum"),
    rolling_avg_cases = ("7day_rolling_avg_cases", "sum"),
    rolling_avg_deaths = ("7day_rolling_avg_deaths", "sum"),
    cumulative_number_cases = ("cumulative_number_cases", "sum"),
    cumulative_number_deaths = ("cumulative_number_deaths", "sum"),
    ).reset_index()

trend_data["date"] = trend_data.date.dt.date

st.sidebar.markdown("Choose a data")
new_cases = sidebar.checkbox("New Cases")
new_deaths = sidebar.checkbox("New Deaths")
new_vaccinations = sidebar.checkbox("New Vaccinations")

st.sidebar.markdown("Choose a format")
rolling_average_cases = sidebar.checkbox("7-Day Rolling Average of Cases")
rolling_average_deaths = sidebar.checkbox("7-Day Rolling Average of Deaths")
cumulative_number_cases = sidebar.checkbox("Cumulative Number of Cases")
cumulative_number_deaths = sidebar.checkbox("Cumulative Number of Deaths")

#graph_format = st.sidebar.selectbox('Choose a format', ('Raw number', '7-day rolling average', 'Cumulated number'))

lines = [new_cases, new_deaths, new_vaccinations, rolling_average_cases, rolling_average_deaths, cumulative_number_cases, cumulative_number_deaths]
line_cols = ["new_cases", "new_deaths", "new_vaccinations", "rolling_average_cases", "rolling_average_deaths", "cumulative_number_cases", "cumulative_number_deaths"]
trends = [c[1] for c in zip(lines,line_cols) if c[0]==True]

ndf = pd.DataFrame(data=trend_data.date.unique(),columns=["date"])

for s in selected:
    new_cols = ["date"]+[f"{s}_{c}" for c in line_cols]
    tdf = trend_data.query(f"location=='{s}'")
    tdf.drop("location", axis=1, inplace=True)
    tdf.columns=new_cols
    ndf=ndf.merge(tdf,on="date",how="inner")
    

new_trends = []
for c in trends:
    new_trends.extend([f"{s}_{c}" for s in selected])

if len(trends)>0:
    #st.markdown("### Trend of Selected Locations")

    fig=ndf.iplot(kind="line", asFigure=True, xTitle="Date", yTitle="Values",
                        x="date", y=new_trends, title=f"Data for {', '.join(trends)}.", subplots=False)
    st.plotly_chart(fig, use_container_width=False)