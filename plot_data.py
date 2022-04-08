import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('COVID Dashboard')
st.markdown('This Dashboard displays the worldwide cases of Covid-19 over time. It is based on the data by Our World in Data. We also have a tutorial on how to build this Dashboard by yourself.')
st.sidebar.title("Category Filter")
#st.sidebar.markdown("Here we will give further information about our project or implement some cool widgets!")

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

dataframe = df["total_cases"]









import streamlit as st
import numpy as np
import pandas as pd
import cufflinks

@st.cache
def get_data(url):
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df.date).dt.date
    df['date'] = pd.DatetimeIndex(df.date)

    return df

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
data = get_data(url)

locations = data.location.unique().tolist()

sidebar = st.sidebar
location_selector = sidebar.selectbox(
    "Select a Location",
    locations
)
st.markdown(f"# Currently Selected {location_selector}")

#trend_level = sidebar.selectbox("Trend Level", ["Daily"])
#st.markdown(f"### Currently Selected {trend_level}")

show_data = sidebar.checkbox("Show Data")

trend_kwds = {"Daily": "1D", "Weekly": "1W", "Monthly": "1M", "Quarterly": "1Q", "Yearly": "1Y"}
trend_data = data.query(f"location=='{location_selector}'").\
    groupby(pd.Grouper(key="date", 
    freq="1D")).aggregate(new_cases=("new_cases", "sum"),
    new_deaths = ("new_deaths", "sum"),
    new_vaccinations = ("new_vaccinations", "sum"),
    new_tests = ("new_tests", "sum")).reset_index()

trend_data["date"] = trend_data.date.dt.date

new_cases = sidebar.checkbox("New Cases")
new_deaths = sidebar.checkbox("New Deaths")
new_vaccinations = sidebar.checkbox("New Vaccinations")
new_tests = sidebar.checkbox("New Tests")

lines = [new_cases, new_deaths, new_vaccinations, new_tests]
line_cols = ["new_cases", "new_deaths", "new_vaccinations", "new_tests"]
trends = [c[1] for c in zip(lines,line_cols) if c[0]==True]

if show_data:
    tcols = ["date"] + trends
    st.dataframe(trend_data[tcols])

daily_cases = data.groupby(pd.Grouper(key="date", freq="1D")).aggregate(new_cases=("new_cases", "sum")).reset_index()
fig = daily_cases.iplot(kind="line", asFigure=True, 
                        x="date", y="new_cases")
st.plotly_chart(fig)
st.markdown("This graph shows Covid-19 new cases per country over time")


subplots=sidebar.checkbox("Show Subplots", True)
if len(trends)>0:
    fig=trend_data.iplot(kind="line", asFigure=True, xTitle="Date", yTitle="Number of new cases",
                         x="date", y=trends, title=f"{trend_level} Trend of {', '.join(trends)}.", subplots=subplots)
    st.plotly_chart(fig, use_container_width=False)

import datetime

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date', today)
end_date = st.sidebar.date_input('End date', tomorrow)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')
