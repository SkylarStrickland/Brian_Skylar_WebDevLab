import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")


'''
key = st.secrets["key"]

genai.configure(api_key=key)
'''
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("hi")
print(response.text)




































































