import google.generativeai as genai
import os
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")



model = genai.GenerativeModel("gemini-1.5-flash")
st.write("Write down a character!")
character = st.text_input("") # NEW 
response = model.generate_content(f"give me background of {character}")

if character == "":
  st.write("")
else:
  st.write(response.text)



































































