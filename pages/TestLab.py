import google.generativeai as genai
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from difflib import get_close_matches

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

DISNEY_API_URL = "http://api.disneyapi.dev/characters"

# Set up retry logic for requests
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))

def fetch_disney_characters(page=1, page_size=50, filters=None):
    try:
        response = session.get(f"{DISNEY_API_URL}?page={page}&pageSize={page_size}")
        response.raise_for_status()
        data = response.json()
        if filters:
            filtered_data = []
            for char in data.get("data", []):
                if filters.get("film") and filters["film"].lower() in [f.lower() for f in char.get("films", [])]:
                    filtered_data.append(char)
                elif filters.get("tv_show") and filters["tv_show"].lower() in [t.lower() for t in char.get("tvShows", [])]:
                    filtered_data.append(char)
            return {"data": filtered_data, "info": data.get("info", {})}
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data: {e}"}

def fetch_filtered_characters(filters=None):
    characters = []
    page = 1
    while True:
        data = fetch_disney_characters(page=page, page_size=50, filters=filters)
        if "error" in data:
            st.error(data["error"])
            return []  # Return an empty list if API fetch fails
        characters.extend(data.get("data", []))
        if not data.get("info", {}).get("nextPage"):
            break
        page += 1
    return characters

def get_character_details(name, filters=None):
    all_characters = fetch_filtered_characters(filters)
    # Find exact or close matches
    character_names = [char["name"] for char in all_characters]
    match = get_close_matches(name, character_names, n=1, cutoff=0.6)
    if match:
        for char in all_characters:
            if char["name"] == match[0]:
                return char
    return None

def generate_specialized_text(character_data):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Write a detailed biography for the Disney character {character_data['name']}, "
            f"including their appearances in films, TV shows, and video games: {character_data}."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating specialized text: {e}"

st.title("Disney Character Explorer")

# Step 1: Ask for filters to narrow the search space
st.subheader("Filter Options (Optional)")
film_filter = st.text_input("Enter a film name (optional):")
tv_filter = st.text_input("Enter a TV show name (optional):")

filters = {}
if film_filter:
    filters["film"] = film_filter
if tv_filter:
    filters["tv_show"] = tv_filter

character_name = st.text_input("Enter a Disney character's name:")

explore_option = st.selectbox(
    "What do you want to know?",
    ["Biography", "Films", "TV Shows", "Video Games"],
)

if character_name:
    character = get_character_details(character_name, filters)

    if not character:
        st.error(f"Character '{character_name}' not found with the provided filters.")
    else:
        st.success(f"Character found: {character['name']}")
        
        if explore_option == "Biography":
            bio = generate_specialized_text(character)
            st.subheader(f"Biography of {character['name']}:")
            st.write(bio)
        else:
            category_data = character.get(explore_option.lower(), [])
            if category_data:
                st.subheader(f"{explore_option} for {character['name']}:")
                st.write(", ".join(category_data))
            else:
                st.warning(f"No {explore_option.lower()} found for {character['name']}.")

st.subheader("Chatbot Interaction")
query = st.text_input("Ask a question about the character:")
if query and character_name and character:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Answer the following question about the Disney character {character['name']}: {query}."
        chatbot_response = model.generate_content(prompt)
        st.write(chatbot_response.text)
    except Exception as e:
        st.error(f"Error in chatbot response: {e}")
