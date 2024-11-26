import google.generativeai as genai
import requests as r
import streamlit as st

genai.configure(api_key="AIzaSyB45quDtyWzRw_ErsU-fxsv_kmytrHLyNM")

DISNEY_API_URL = "https://api.disneyapi.dev/character"

st.sidebar.title("Filter Your Disney Character")
tv_show_filter = st.sidebar.text_input("Enter a Disney TV show:")
num_video_games = st.sidebar.slider("Minimum number of video games appearances:", 0, 10, 0)
has_park_attractions = st.sidebar.radio("Is the character featured in park attractions?", ["No", "Yes"])

st.title("Disney Character Explorer")
st.write("---")

aDict = {}

def fetch_and_filter_characters():
    try:
        response = r.get(f"{DISNEY_API_URL}?tvShows={tv_show_filter.replace(' ', '%20')}")
        response.raise_for_status()
        data = response.json()
        for char in data["data"]:
            num_video_game_appearances = len(char.get("videoGames", []))
            in_park_attractions = len(char.get("parkAttractions", [])) > 0
            if has_park_attractions == "No" and not in_park_attractions and num_video_game_appearances >= num_video_games:
                aDict[char["name"]] = {
                    "tvShows": char["tvShows"],
                    "videoGames": char["videoGames"],
                    "parkAttractions": char["parkAttractions"]
                }
            elif has_park_attractions == "Yes" and in_park_attractions and num_video_game_appearances >= num_video_games:
                aDict[char["name"]] = {
                    "tvShows": char["tvShows"],
                    "videoGames": char["videoGames"],
                    "parkAttractions": char["parkAttractions"]
                }
    except r.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from Disney API: {e}")
    except KeyError as e:
        st.error(f"Unexpected response structure: {e}")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

if tv_show_filter:
    fetch_and_filter_characters()
    if not aDict:
        st.write("No characters match your filters. Try adjusting them.")
        selected_character = None
    else:
        selected_character = st.selectbox("Select a character to explore:", list(aDict.keys()))
        if selected_character:
            char_data = aDict[selected_character]
            st.subheader(f"Character: {selected_character}")
            st.write("### TV Shows")
            st.write(", ".join(char_data["tvShows"]) or "None")
            st.write("### Video Games")
            st.write(", ".join(char_data["videoGames"]) or "None")
            st.write("### Park Attractions")
            st.write(", ".join(char_data["parkAttractions"]) or "None")
            st.write("---")
else:
    st.write("Enter a TV show to start filtering.")
    selected_character = None

if selected_character:
    st.subheader("Character Biography–don't forget to ask questions at the end!")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        char_data = aDict[selected_character]
        prompt = (
            f"Write a detailed biography for the Disney character {selected_character}, "
            f"based on their TV shows, video games, and park attractions: {char_data}."
        )
        response = model.generate_content(prompt)
        if not response.text.strip():
            st.warning("No biography could be generated. Please try again with a different character.")
        else:
            st.write(response.text)
    except genai.exceptions.RateLimitError:
        st.warning("Rate limit reached. Please try again later.")
    except genai.exceptions.AuthenticationError:
        st.error("Authentication error with Google Gemini API. Please check your API key.")
    except Exception as e:
        st.error(f"Error generating biography: {e}")

if selected_character:
    st.subheader("Chatbot Interaction")
    query = st.text_input("Ask a question about the character:")
    if query:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            char_data = aDict[selected_character]
            prompt = (
                f"Answer the following question about the Disney character {selected_character}: {query}. "
                f"Use their TV shows, video games, and park attractions for context: {char_data}."
            )
            chatbot_response = model.generate_content(prompt)
            if not chatbot_response.text.strip():
                st.warning("The chatbot was unable to generate a response. Please refine your question.")
            else:
                st.write(chatbot_response.text)
        except genai.exceptions.RateLimitError:
            st.warning("Rate limit reached. Please try again later.")
        except genai.exceptions.AuthenticationError:
            st.error("Authentication error with Google Gemini API. Please check your API key.")
        except Exception as e:
            st.error(f"Error in chatbot response: {e}")
