import google.generativeai as genai
import os
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

model = genai.GenerativeModel("gemini-1.5-flash")
st.write("Write down a character!")
character = st.text_input("") # NEW 
inputRequest = f"give me background of {character}"
response = model.generate_content(inputRequest)

if character == "":
  st.write("")
else:
  st.write(inputRequest)
  st.write(response.text)

