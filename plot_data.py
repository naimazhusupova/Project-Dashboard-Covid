import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('COVID Dashboard')
st.header('Global Covid-19 cases')
st.markdown('This Graph displays the worldwide cases of Covid-19 over time')

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

dataframe = df["total_cases"]

st.line_chart(dataframe)

st.header('Covid-19 new cases')
st.write('This is a graph of new Covid-19 cases')
df1 = df["new_cases"]

st.line_chart(df1)

st.header('Total Covid-19 cases per continent')
st.write('This Graph shows Covid-19 total cases dynamics per continent')
df2 = df['continent'].value_counts().head(10).sort_values(ascending=False)
st.area_chart(df2)

