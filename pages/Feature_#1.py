import streamlit as st
import pandas as pd
import numpy as np
import openai

# Set up OpenAI API key
openai.api_key = 'APIkey'

# Header and Sidebar
st.sidebar.markdown("# Prototype Demonstration #2")

message = "This page provides our first example for Prototype #1!\n"
message += "Please let us know how we can improve this going forward. Thank you!"
st.write(message)

# Functional Feature #1: Chatbot (ChatGPT-style UI)
st.subheader('Functional Feature #1: Chatbot!', divider='grey')

# Function to get chatbot response from OpenAI
def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# ChatGPT-like chat interface
user_input = st.chat_input("Ask the assistant anything about grant administration:")
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