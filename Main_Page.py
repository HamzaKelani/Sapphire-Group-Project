import streamlit as st
import pandas as pd
import numpy as np
import time

st.markdown("# Prototype V1")
st.sidebar.markdown("# Prototype V1")

message = "This page provides our first example for Prototype #1!\n"
message += "Please let us know how we can improve this going forward. Thank you!"
st.write(message)

st.subheader('Functional Feature #1: Citizen Reporting System!', divider='grey')
df = pd.DataFrame(
    np.random.randn(0, 2) / [50, 50] + [37.33, -121.88],
    columns=['lat', 'lon'])
n = 0
if prompt:= st.text_input("What is the address of the location where you have located the trash?"):
    st.write(f"A User has reported trash at the address: {prompt}")
    n += 1
    df = pd.DataFrame(
    np.random.randn(n, 2) / [50, 50] + [37.33, -121.88],
    columns=['lat', 'lon'])
    st.balloons()
st.map(df)


st.subheader('Functional Feature #2: Live-feed Cameras With Sensor Technology!', divider='grey')
VIDEO_URL = "https://www.youtube.com/watch?v=N1qrW_7GDpc"
st.video(VIDEO_URL)

st.subheader('Functional Feature #3: View All Currently Reported Locations!', divider='grey')
df = pd.DataFrame(
    np.random.randn(50, 2) / [50, 50] + [37.33, -121.88],
    columns=['lat', 'lon'])
st.map(df)

