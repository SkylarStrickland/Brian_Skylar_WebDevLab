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

# Configure the Gemini API key
genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")
model = genai.GenerativeModel("gemini-1.5-flash")

# App title and description
st.title("💬 Google Gemini Chatbot")
st.write(
    "This chatbot uses Google's Gemini AI model to generate responses. "
    "To use this app, simply type your message below."
)

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user prompt
if prompt := st.chat_input("Enter your message here:"):
    # Store and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Google Gemini
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)

    # Store the assistant's response in session state
    st.session_state.messages.append({"role": "assistant", "content": response.text})



































































