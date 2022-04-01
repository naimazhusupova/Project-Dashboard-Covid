import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

dataframe = df["total_cases"]

st.line_chart(dataframe)