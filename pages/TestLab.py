import google.generativeai as genai
import requests
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

DISNEY_API_URL = "http://api.disneyapi.dev/characters"

def fetch_disney_characters(page=1, page_size=10):
    try:
        response = requests.get(f"{DISNEY_API_URL}?page={page}&pageSize={page_size}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data: {e}"}

def get_character_details(name):
    data = fetch_disney_characters()
    if "error" in data:
        return data["error"]
    characters = data.get("data", [])
    for char in characters:
        if char["name"].lower() == name.lower():
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

character_name = st.text_input("Enter a Disney character's name:")

explore_option = st.selectbox(
    "What do you want to know?",
    ["Biography", "Films", "TV Shows", "Video Games"],
)

if character_name:
    character = get_character_details(character_name)

    if not character:
        st.error(f"Character '{character_name}' not found.")
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
