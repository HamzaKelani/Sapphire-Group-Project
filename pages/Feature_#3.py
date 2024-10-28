import streamlit as st
import pandas as pd
import numpy as np
import openai
import os as os
from openai import OpenAI

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Header and Sidebar
st.sidebar.markdown("# Prototype Demonstration #3")

message = "This page provides our 3rd feature for Prototype #1!\n"
message += "We help students improve their essay before submission, allowing them to have a better chance at landing the grant ahead of other students."
st.write(message)

# Functional Feature #1: Chatbot (ChatGPT-style UI)
st.subheader('Functional Feature #1: Chatbot!', divider='grey')

# Function to get chatbot response from OpenAI
def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Act as an expert student essay advisor to elevate this essay to a clear, upper-college level. Focus on impactful, concise language that meets all grant requirements. Highlight key achievements, motivations, and goals in two five-sentence paragraphs, ensuring each sentence adds value and depth."
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
user_input = st.text_input("Input your essay + the grant you are applying for, and we will provide an improvised version of your essay:")
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