import streamlit as st
import pandas as pd
import numpy as np
import openai
import os as os
import fitz  # PyMuPDF
from openai import OpenAI

st.image("https://i.ibb.co/wCV0SFw/grantednow.png")
st.logo(image="https://i.ibb.co/wCV0SFw/grantednow.png")

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

xl = pd.ExcelFile("GrantedNow.xlsx")
StudentDoc = xl.parse("Sheet1")

st.sidebar.markdown("GrantedNow!")

st.subheader('', divider='grey')
st.subheader('Analyze Application', divider='grey')

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai

def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts information exactly as it appears in the provided text. "
                    "Using the input below, identify and extract details precisely as they are written. "
                    "If any detail is missing, omit it and do not assume or create information."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Extract the following details from the text exactly as they appear:\n\n"
                    f"{user_input}\n\n"
                    "Required categories:\n"
                    "1. Name\n"
                    "2. Gender\n"
                    "3. Age\n"
                    "4. California School\n"
                    "5. Major\n"
                    "6. Race\n"
                    "7. Ethnicity\n"
                    "8. 'Tell us why you believe you deserve this grant. What experiences, skills, "
                    "or challenges have shaped you, and how do these make you stand out as a candidate for our support?'"
                    "\n\nPlease return the information in this format, strictly without creating or assuming details."
                )
            }
        ]
    )
    return response.choices[0].message.content

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
text = ''

if uploaded_file is not None:
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    for i in range(len(pdf)):
        page = pdf.load_page(i)
        text = page.get_text("text")
        
        st.markdown(f"<h3 style='font-size: 24px; font-weight: bold; text-decoration: underline;'>Content of Application:</h3>", unsafe_allow_html=True)
        st.write(text)
        
        summary = get_chatbot_response(text)
        st.markdown(f"<h3 style='font-size: 24px; font-weight: bold; text-decoration: underline;'>Summary of Application:</h3>", unsafe_allow_html=True)
        st.write(summary)

st.subheader('', divider='grey')
st.subheader('Compare Students', divider='grey')

studentNames = StudentDoc[['Name']]
chooseStudent = st.selectbox("Select a student to compare to:", studentNames)
if chooseStudent:
    # Print or display the selected student's data
    selectedStudentData = StudentDoc[StudentDoc['Name'] == chooseStudent].iloc[[0]]
    # Extract data from the selected student's row
    name = selectedStudentData['Name'].values[0]
    gender = selectedStudentData['Gender'].values[0]
    age = selectedStudentData['Age'].values[0]
    school = selectedStudentData['California School'].values[0]
    major = selectedStudentData['Major'].values[0]
    race = selectedStudentData['Race'].values[0]
    ethnicity = selectedStudentData['Ethnicity'].values[0]
    grantReason = selectedStudentData['Tell us why you believe you deserve this grant. What experiences, skills, or challenges have shaped you, and how do these make you stand out as a candidate for our support?\n(1 Paragraphs, 6 Sentances Each)'].values[0]
    user_input = f"""
    Selected Student's Information:\n
    1. Name: {name}
    2. Gender: {gender}
    3. Age: {age}
    4. California School: {school}
    5. Major: {major}
    6. Race: {race}
    7. Ethnicity: {ethnicity}
    8. Why: {grantReason}\n
"""
    
st.write(user_input)

st.subheader('', divider='grey')
st.subheader('Decision Opinion', divider='grey')

def get_decision_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the ultimate decision maker on accepting someone to the grant program. You need to be extremely tough as there are only 4 spots, and based on the quality of the application you read, being in a STEM major, the age of the user and the believability of their"
                    "circumstances, give a decision on if you would accept them or not. Write a 1 paragraph, 5 sentance response, and state at the start 'I would' or 'I would not' grant this student acceptance into the program."
                )
            },
            {
                "role": "user",
                "content": (user_input)
            }
        ]
    )
    return response.choices[0].message.content

decision = get_decision_response(user_input)
st.write(decision)
