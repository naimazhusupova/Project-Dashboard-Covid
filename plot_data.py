import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

st.title('COVID-19 Dashboard')
st.markdown('This Dashboard displays the worldwide cases and deaths of Covid-19 over time. It is based on the data by Our World in Data. This includes the information about positive cases, deaths and vaccinations per country.')
st.sidebar.title("Category Filter")
st.sidebar.markdown("Please choose your options for data display")

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

#removing Continents and other unwanted categories from the country selection list
locations_to_remove = ['Africa', 'Asia', 'Australia', 'Europe', 'European Union', 'High income', 'International', 'Low income',
 'Lower middle income', 'Oceania', 'South America', 'Upper middle income', 'World']

for loc in locations_to_remove:
    locations.remove(loc)

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
df['7day_rolling_avg_cases_per_million'] = df['new_cases_per_million'].rolling(window=7).mean()
df['7day_rolling_avg_deaths_per_million'] = df['new_deaths_per_million'].rolling(window=7).mean()
df['7day_rolling_avg_vaccinations_per_million'] = df['new_vaccinations_smoothed_per_million'].rolling(window=7).mean()
df['cumulative_number_cases_per_million'] = df['new_cases_per_million'].cumsum(axis = 0)
df['cumulative_number_deaths_per_million'] = df['new_deaths_per_million'].cumsum(axis = 0)
df['cumulative_number_vaccinations_per_million'] = df['new_vaccinations_smoothed_per_million'].cumsum(axis = 0)

selected = sidebar.multiselect("Choose a location", locations)
st.markdown(f"### You Selected: {', '.join(selected)}")

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


#selected_type = sidebar.selectbox("Choose a data type", ["New Cases", "New Deaths", "New Vaccinations"])

selected_type1 = sidebar.radio("Choose a data type", ["New Cases", "New Deaths", "New Vaccinations"])

m = 0
print(selected_type1)
if selected_type1 == "New Cases":
    m = 0
if selected_type1 == "New Deaths":
    m = 1
if selected_type1 == "New Vaccinations":
    m = 2



selected_type2 = sidebar.radio("Choose a data format", ["Raw Number per Million", "7-Day Rolling Average per Million", "Cumulative Number per Million"])

n = 0
print(selected_type2)
if selected_type2 == "Raw Number per Million":
    n = 0
if selected_type2 == "7-Day Rolling Average per Million":
    n = 1
if selected_type2 == "Cumulative Number per Million":
    n = 2


mn = 3*n+m

print(mn)
print(mn)
print(mn)
print(mn)
print(mn)


lines = [False for i in range(9)]
lines[mn] = True
line_cols = ["new_cases_per_million", "new_deaths_per_million", "new_vaccinations_smoothed_per_million", "rolling_average_cases_per_million", "rolling_average_deaths_per_million", "rolling_average_vaccinations_per_million", "cumulative_number_cases_per_million", "cumulative_number_deaths_per_million", "cumulative_number_vaccinations_per_million"]
trends = [c[1] for c in zip(lines,line_cols) if c[0]==True]


print(lines)
print(lines)
print(lines)
print(lines)
print(lines)

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
    
    fig = plt.figure(figsize=(7,4))
    ax = fig.add_subplot(1,1,1)
    for _ in range(0,len(new_trends)):
        ax.plot(ndf["date"],ndf[new_trends[_]], label=new_trends[_])
    
    ax.set_xlabel("Date")
    ax.set_ylabel(selected_type1 +' '+ selected_type2)
    ax.xaxis.grid(True, linestyle='--')
    ax.yaxis.grid(True, linestyle='--')
    ax.legend(loc="upper left")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    st.plotly_chart(fig, use_container_width=False)

    st.markdown(f"### Peak values:")
    for _ in range(0,len(new_trends)):
        st.markdown("Peak value for "+new_trends[_]+": "+str(int(ndf[new_trends[_]].max()))+" ,  date: "+str(ndf["date"][ndf[new_trends[_]].idxmax()]))


    print(list(new_trends))


    
