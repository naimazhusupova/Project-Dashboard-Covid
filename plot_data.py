import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cufflinks
import datetime
import re
import base64

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

analysis_type = sidebar.radio("Analysis Type", ["Single", "Multiple"])
st.markdown(f"Analysis Mode: {analysis_type}")

if analysis_type=="Single":
    location_selector = sidebar.selectbox(
        "Select a Location",
        locations
    )
    st.markdown(f"### Currently Selected {location_selector}")
    #trend_level = sidebar.selectbox("Trend Level", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
    #st.markdown(f"### Currently Selected {trend_level}")

    #show_data = sidebar.checkbox("Show Data")

    #trend_kwds = {"Daily": "1D", "Weekly": "1W", "Monthly": "1M", "Quarterly": "1Q", "Yearly": "1Y"}
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

    #if show_data:
    #    tcols = ["date"] + trends
    #    st.dataframe(trend_data[tcols])

    #subplots=sidebar.checkbox("Show Subplots", True)
    if len(trends)>0:
        fig=trend_data.iplot(kind="line", asFigure=True, xTitle="Date", yTitle="Values",
                            x="date", y=trends, title=f"Trend of {', '.join(trends)}.", subplots=False)
        st.plotly_chart(fig, use_container_width=False)

if analysis_type=="Multiple":
    selected = sidebar.multiselect("Select Locations ", locations)
    st.markdown(f"### Selected Locations: {', '.join(selected)}")
    #show_data = sidebar.checkbox("Show Data")
    #trend_level = sidebar.selectbox("Trend Level", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
    #st.markdown(f"### Currently Selected {trend_level}")

    #trend_kwds = {"Daily": "1D", "Weekly": "1W", "Monthly": "1M", "Quarterly": "1Q", "Yearly": "1Y"}

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

    #if show_data:
    #    if len(ndf)>0:
    #        st.dataframe(ndf)
    #    else:
    #        st.markdown("Empty Dataframe")

    new_trends = []
    for c in trends:
        new_trends.extend([f"{s}_{c}" for s in selected])

    #subplots=sidebar.checkbox("Show Subplots", True)
    if len(trends)>0:
        st.markdown("### Trend of Selected Locations")

        fig=ndf.iplot(kind="line", asFigure=True, xTitle="Date", yTitle="Values",
                            x="date", y=new_trends, title=f"Trend of {', '.join(trends)}.", subplots=False)
        st.plotly_chart(fig, use_container_width=False)



#
#
#
#


def df_filter(message,df):

        slider_1, slider_2 = st.slider('%s' % (message),0,len(df)-1,[0,len(df)-1],1)

        while len(str(df.iloc[slider_1][1]).replace('.0','')) < 4:
            df.iloc[slider_1,1] = '0' + str(df.iloc[slider_1][1]).replace('.0','')
            
        while len(str(df.iloc[slider_2][1]).replace('.0','')) < 4:
            df.iloc[slider_2,1] = '0' + str(df.iloc[slider_1][1]).replace('.0','')

        start_date = datetime.datetime.strptime(str(df.iloc[slider_1][0]).replace('.0','') + str(df.iloc[slider_1][1]).replace('.0',''),'%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
        
        end_date = datetime.datetime.strptime(str(df.iloc[slider_2][0]).replace('.0','') + str(df.iloc[slider_2][1]).replace('.0',''), '%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        st.info('Start: **%s** End: **%s**' % (start_date,end_date))
        
        filtered_df = df.iloc[slider_1:slider_2+1][:].reset_index(drop=True)

        return filtered_df


def download_csv(name,df):
    
    csv = df.to_csv(index=False)
    base = base64.b64encode(csv.encode()).decode()
    file = (f'<a href="data:file/csv;base64,{base}" download="%s.csv">Download file</a>' % (name))
    
    return file

if __name__ == '__main__':

    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    df = df['date']
    st.title('Datetime Filter')
    filtered_df = df_filter('Move sliders to filter dataframe',df)

    column_1, column_2 = st.beta_columns(2)

    with column_1:
        st.title('Data Frame')
        st.write(filtered_df)

    with column_2:
        st.title('Chart')
        st.line_chart(filtered_df['value'])

    st.markdown(download_csv('Filtered Data Frame',filtered_df),unsafe_allow_html=True)