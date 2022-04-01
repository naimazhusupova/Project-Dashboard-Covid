import streamlit as st
import pandas as pd
import numpy as np

st.title('COVID Dashboard')
st.header('Global Covid-19 cases')
st.markdown('This Graph displays the worldwide cases of Covid-19 over time')

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

dataframe = df["total_cases"]

st.line_chart(dataframe)
