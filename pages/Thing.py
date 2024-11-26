import google.generativeai as genai
import os
import streamlit as st

# genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")



# model = genai.GenerativeModel("gemini-1.5-flash")
# st.write("Write down a character!")
# character = st.text_input("") # NEW 
# response = model.generate_content(f"give me background of {character}")

# if character == "":
#   st.write("")
# else:
#   st.write(response.text)

import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.write(message)

# Input field for user prompt
prompt = st.text_input("Enter your message here:")
if st.button("Send") and prompt:
    # Add user's message to chat history
    st.session_state.messages.append(f"You: {prompt}")
    st.write(f"You: {prompt}")

    # Generate response
    response = model.generate_content(prompt)
    st.session_state.messages.append(f"Gemini: {response.text}")
    st.write(f"Gemini: {response.text}")
