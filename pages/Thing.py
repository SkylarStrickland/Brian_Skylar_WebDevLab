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


DISNEY_API_URL = "http://api.disneyapi.dev/characters"

def fetch_disney_characters(page=1, page_size=10):
    try:
        response = requests.get(f"{DISNEY_API_URL}?page={page}&pageSize={page_size}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch dat: {e}"}

def get_character_details(name):
    data = fetch_disney_characters()
    if "error" in data:
        return data["error"]
    characters = data["data"]
    for char in characters:
        if char["name"].lower() == name.lower():
            return char
    return f"Character '{name}' not found."

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

def disney_chatbot(query, character_data):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Answer the following question about the Disney character {character_data['name']}: {query}."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error in chatbot response: {e}"

if __name__ == "__main__":
    print("Welcome to the Disney Character Explorer!")
    character_name = input("Enter the name of a Disney character: ")
    character = get_character_details(character_name)

    if isinstance(character, str):
        print(character)
    else:
        print(f"Character found: {character['name']}")
        print(f"Generating specialized text for {character['name']}...")
        bio = generate_specialized_text(character)
        print("Specialized Text:\n", bio)

        while True:
            user_query = input("Ask a question about this character (or type 'exit' to quit): ")
            if user_query.lower() == "exit":
                break
            response = disney_chatbot(user_query, character)
            print("Chatbot Response:\n", response)

































































