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

import google.generativeai as genai
import streamlit as st

# Configure the API key
genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# App title
st.title("Character Background Generator")

# Input field for the user's character prompt
character = st.text_input("Enter a character to generate their background:")

# Generate response and update chat history
if st.button("Generate Background"):
    if character:
        # Call the model to generate a response
        response = model.generate_content(f"Give me the background of {character}")
        # Add input and response to chat history
        st.session_state.chat_history.append({"question": character, "response": response.text})
    else:
        st.warning("Please enter a character.")

# Display chat history
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['question']}")
    st.markdown(f"**Gemini:** {chat['response']}")



































































