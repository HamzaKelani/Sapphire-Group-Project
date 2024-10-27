import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import os


message = "This page provides our user with information regarding grants!\n"
message += "Link a page from a notable grant, and receive a summary regarding who is eligible!"
st.write(message)
# Create a text input for the URL
url = st.text_input('Enter a URL')

def get_web_content(url):
    # Fetch the webpage
    web_content = ""
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Display the text of the webpage
    st.write('Here is an in-depth summary of this grant:')
    article_tags = soup.find_all('article')
    
    for article in article_tags:
        paragraphs = article.find_all('p')
        for p in paragraphs:
            web_content = web_content + str(p.get_text()) + '\n'

    return web_content

# Takes the transcription of the meeting and returns a summary of it via text completions
def abstract_summary_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Analyze the following webpage about student grants and provide a concise summary in bullet-point format. Ensure the information is clear, factual, and covers the key points accurately. Include details such as eligibility criteria, application deadlines, available grant amounts, required documents, and any notable conditions or limitations. Present the information as a list of bullet points, aiming for brevity and clarity. Please include the grant name before all the bullet points"
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Create a button to fetch the content
if st.button('Fetch Content'):
    display_content = get_web_content(url)
    st.write(abstract_summary_extraction(display_content))