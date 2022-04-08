import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cufflinks
import datetime

st.title('COVID Dashboard')
st.markdown('This Dashboard displays the worldwide cases of Covid-19 over time. It is based on the data by Our World in Data. We also have a tutorial on how to build this Dashboard by yourself.')
st.sidebar.title("Category Filter")
#st.sidebar.markdown("Here we will give further information about our project or implement some cool widgets!")

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

analysis_type = sidebar.radio("Analysis Type", ["Multiple"])

if analysis_type=="Multiple":
    selected = sidebar.multiselect("Select Locations ", locations)
    st.markdown(f"### Selected Locations: {', '.join(selected)}")

    trend_data = data.query(f"location in {selected}").\
        groupby(["location", pd.Grouper(key="date", 
        freq="1D")]).aggregate(new_cases=("new_cases", "sum"),
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
        st.markdown("### Trend of Selected Locations")

        fig=ndf.iplot(kind="line", asFigure=True, xTitle="Date", yTitle="Values",
                            x="date", y=new_trends, title=f"Trend of {', '.join(trends)}.", subplots=False)
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

