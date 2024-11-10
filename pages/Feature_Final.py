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

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Load the PDF
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Analyze the PDF
    for i in range(len(pdf)):
        page = pdf.load_page(i)
        text = page.get_text("text")
        st.write(f"Content of Page {i+1}:")
        st.write(text)

st.subheader(' ', divider='grey')

# Function to get chatbot response from OpenAI
def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Using a student’s SAI score as input, provide a list of eligible grants, including the grant name, description, eligibility criteria, award amount, and application deadlines. Consider federal, state, and private grants, tailoring results to the financial need indicated by the SAI score. Act as if you only operate in California. Please add a link to each grant website at the bottom of the message."
            },
            {
                "role": "user",
                "content": "prompt"
            }
        ]
    )
    return response.choices[0].message.content

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# ChatGPT-like chat interface
user_input = st.selectbox("Choose your SAI score, and in return receive a list of grants you are eligible to receive:", options=["-15,000 -> -10,000", "-10,000 -> -5,000", "-5,000 -> 0", " 0 -> 2,000", "5,000 -> 10,000"])
if user_input:
    # Add user message to the chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Get response from chatbot
    response = get_chatbot_response(user_input)
    
    # Add assistant's response to the chat history
    st.session_state['messages'].append({"role": "assistant", "content": response})

# Display chat history in a ChatGPT-like UI
for message in st.session_state['messages']:
    if message['role'] == "user":
        with st.chat_message("user"):
            st.write(message['content'])
    else:
        with st.chat_message("assistant"):
            st.write(message['content'])