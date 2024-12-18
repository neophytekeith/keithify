import streamlit as st
import requests
import re

# Set your API key and host URL
API_KEY = "d90a09a015msh12f69eb58ce9364p149b89jsnd92118bd82d3"  # Replace with your actual RapidAPI key
API_HOST = "youtube-mp36.p.rapidapi.com"

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    # Try to match either of the common YouTube URL formats
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to convert video to MP3 using external API
def convert_to_mp3(video_url):
    api_url = "https://youtube-mp36.p.rapidapi.com/dl"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    # Extract the video ID from the URL
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Invalid YouTube URL"

    # Set the query string with the extracted video ID
    querystring = {"id": video_id}
    
    try:
        response = requests.get(api_url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == "ok":
                return data['title'], data['link']
            else:
                return None, data.get('msg', 'Unknown error occurred.')
        else:
            return None, f"HTTP Error: {response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        # Call the external API to convert video to MP3
        song_title, download_link = convert_to_mp3(url)
        if song_title:
            st.success(f"Conversion successful! You can download the MP3 below.")
            st.write(f"Song Title: {song_title}")
            st.markdown(f"[Download MP3]({download_link})")
        else:
            st.error(f"Error: {download_link}")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Optional: "Reset Conversion" button to clear fields
if st.button("Reset Conversion"):
    st.experimental_rerun()  # Refresh the app to reset the URL input
