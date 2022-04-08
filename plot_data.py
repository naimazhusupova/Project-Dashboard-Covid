import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('COVID Dashboard')
st.header('Global Covid-19 cases')
st.sidebar.title("About this dashboard Project")
st.markdown('This Graph displays the worldwide cases of Covid-19 over time')
st.sidebar.markdown("Here we will give further information about our project or implement some cool widgets!")

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

daily_cases = data.groupby(pd.Grouper(key="date", freq="1D")).aggregate(new_cases=("new_cases", "sum")).reset_index()
fig = daily_cases.iplot(kind="line", asFigure=True, 
                        x="date", y="new_cases")
#st.plotly_chart(fig)












import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)


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

daily_cases = data.groupby(pd.Grouper(key="date", freq="1D")).aggregate(new_cases=("new_cases", "sum")).reset_index()
fig = daily_cases.iplot(kind="line", asFigure=True, 
                        x="date", y="new_cases")
st.plotly_chart(fig)




