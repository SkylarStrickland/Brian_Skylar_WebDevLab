import streamlit as st
import os
import requests as r

baseUrl = "https://api.disneyapi.dev/character"

# Creating the Sidebar

st.sidebar.title("Pick your Disney Character")
movie = st.sidebar.text_input("Enter in your favorite Disney Movie!").replace(" ", "%20") # NEW 


hasEnemies = st.sidebar.radio("Does your character have enemies?", ["No", "Yes"]) # NEW

inputNumFilms = int(st.sidebar.number_input("How many films has this character starred in?", min_value=1, max_value = 10, value=1))# NEW



# Header

st.header("Suitable Disney Characters!")
st.write("---")



# Parsing through the API

aDict = {}
def getData(url):
    b = r.get(url + "&pageSize=infty").json()
    
    for charDict in b["data"]:
        numFilms = len(charDict["films"])
        if hasEnemies == "No":
            if len(charDict["enemies"]) == 0 and numFilms >= inputNumFilms:
                name = charDict["name"]
                listFilms = charDict["films"]
                imgUrl = charDict["imageUrl"]
                aDict[name] = (listFilms, imgUrl)
        else:
            if len(charDict["enemies"]) != 0 and numFilms >= inputNumFilms:
                name = charDict["name"]
                listFilms = charDict["films"]
                imgUrl = charDict["imageUrl"]
                aDict[name] = (listFilms, imgUrl)

if movie == "":
    st.write("Write something in!")

else:
    try:
        movieUrl = baseUrl + f"?films={movie}"
        getData(movieUrl)
        if aDict == {}:
            st.write("bruh u got nothing")

        for name, (listFilms, imgUrl) in aDict.items():
            st.header(f"Your Disney Character is {name}")
            st.image(imgUrl, width = 300)
            st.write("---")

    except: # if retrieving data from getData() results in an error
        st.write("so it actually didn't work and you got nothing")

