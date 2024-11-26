import google.generativeai as genai
import requests as r
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

DISNEY_API_URL = "https://api.disneyapi.dev/character"

# Sidebar Inputs
st.sidebar.title("Filter Your Disney Character")
movie_filter = st.sidebar.text_input("Enter your favorite Disney movie:")
num_films = st.sidebar.slider("Minimum number of films:", 1, 10, 1)
has_enemies = st.sidebar.radio("Does the character have enemies?", ["No", "Yes"])

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
            has_enemies_check = len(char.get("enemies", [])) > 0

            if has_enemies == "No" and not has_enemies_check and num_films_appearances >= num_films:
                aDict[char["name"]] = {
                    "films": char["films"],
                    "tvShows": char["tvShows"],
                    "allies": char["allies"],
                    "enemies": char["enemies"]
                }
            elif has_enemies == "Yes" and has_enemies_check and num_films_appearances >= num_films:
                aDict[char["name"]] = {
                    "films": char["films"],
                    "tvShows": char["tvShows"],
                    "allies": char["allies"],
                    "enemies": char["enemies"]
                }
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

# Display Data
if movie_filter:
    fetch_and_filter_characters()
    if not aDict:
        st.write("No characters match your filters. Try adjusting them.")
        selected_character = None
    else:
        selected_character = st.selectbox("Select a character to explore:", list(aDict.keys()))
        if selected_character:
            char_data = aDict[selected_character]
            st.subheader(f"Character: {selected_character}")
            st.write("### Films")
            st.write(", ".join(char_data["films"]) or "None")
            st.write("### TV Shows")
            st.write(", ".join(char_data["tvShows"]) or "None")
            st.write("### Allies")
            st.write(", ".join(char_data["allies"]) or "None")
            st.write("### Enemies")
            st.write(", ".join(char_data["enemies"]) or "None")
            st.write("---")
else:
    st.write("Enter a movie to start filtering.")
    selected_character = None

# Specialized Content Generation
if selected_character:
    st.subheader("Generate a Character Biography")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        char_data = aDict[selected_character]
        prompt = (
            f"Write a detailed biography for the Disney character {selected_character}, "
            f"based on their films, TV shows, allies, and enemies: {char_data}."
        )
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating biography: {e}")

# Chatbot Interaction
if selected_character:
    st.subheader("Chatbot Interaction")
    query = st.text_input("Ask a question about the character:")
    if query:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            char_data = aDict[selected_character]
            prompt = (
                f"Answer the following question about the Disney character {selected_character}: {query}. "
                f"Use their films, TV shows, allies, and enemies for context: {char_data}."
            )
            chatbot_response = model.generate_content(prompt)
            st.write(chatbot_response.text)
        except Exception as e:
            st.error(f"Error in chatbot response: {e}")
