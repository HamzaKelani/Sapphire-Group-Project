import streamlit as st
import pandas as pd
import numpy as np
import openai
import os as os
import fitz  # PyMuPDF
from openai import OpenAI

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

xl = pd.ExcelFile("GrantedNow.xlsx")
StudentDocs = xl.parse("Sheet1")

st.sidebar.markdown("GrantedNow!")

message = "Please let us know how we can improve this going forward. Thank you!"
st.write(message)

st.subheader('Analyze Application', divider='grey')

import openai
import os

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Assuming `client` is initialized properly as your OpenAI client wrapper:
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

if uploaded_file is not None:
    # Load the PDF
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Analyze the PDF
    for i in range(len(pdf)):
        page = pdf.load_page(i)
        text = page.get_text("text")
        
        # Display original text
        st.write(f"Content of Page {i+1}:")
        st.write(text)
        
        # Generate and display summary for each page
        summary = get_chatbot_response(text)
        st.write(f"Summary of Page {i+1}:")
        st.write(summary)

st.subheader(' ', divider='grey')
