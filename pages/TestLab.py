import google.generativeai as genai
import requests as r
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

DISNEY_API_URL = "https://api.disneyapi.dev/character"

# Sidebar Inputs
st.sidebar.title("Filter Your Disney Character")
movie_filter = st.sidebar.text_input("Enter your favorite Disney movie:")
num_films = st.sidebar.slider("Minimum number of films:", 1, 10, 1)
has_allies = st.sidebar.radio("Does the character have allies?", ["No", "Yes"])

# Header
st.title("Disney Character Explorer")
st.write("---")

# Fetch and Filter API Data
aDict = {}
def fetch_and_filter_characters():
    try:
        response = r.get(f"{DISNEY_API_URL}?films={movie_filter.replace(' ', '%20')}").json()
        for char in response["data"]:
            num_films_appearances = len(char.get("films", []))
            has_allies_check = len(char.get("allies", [])) > 0

            if has_allies == "No" and not has_allies_check and num_films_appearances >= num_films:
                aDict[char["name"]] = (char["films"], char["imageUrl"])
            elif has_allies == "Yes" and has_allies_check and num_films_appearances >= num_films:
                aDict[char["name"]] = (char["films"], char["imageUrl"])
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

# Display Data
if movie_filter:
    fetch_and_filter_characters()
    if not aDict:
        st.write("No characters match your filters. Try adjusting them.")
    else:
        for name, (films, img_url) in aDict.items():
            st.header(f"Character: {name}")
            st.image(img_url, width=300)
            st.subheader("Films:")
            st.write(", ".join(films) or "None")
            st.write("---")
else:
    st.write("Enter a movie to start filtering.")

# Specialized Content Generation
st.subheader("Generate a Character Biography")
selected_character = st.selectbox("Select a character to generate their biography:", list(aDict.keys()))
if selected_character:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        character_data = aDict[selected_character]
        prompt = f"Write a detailed biography for the Disney character {selected_character}, based on the films: {', '.join(character_data[0])}."
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating biography: {e}")

# Chatbot Interaction
st.subheader("Chatbot Interaction")
query = st.text_input("Ask a question about the character:")
if query and selected_character:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Answer the following question about the Disney character {selected_character}: {query}."
        chatbot_response = model.generate_content(prompt)
        st.write(chatbot_response.text)
    except Exception as e:
        st.error(f"Error in chatbot response: {e}")
