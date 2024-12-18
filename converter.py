import streamlit as st
import requests
import re

# Set your API key and host URL
API_KEY = "3d094d7278msh8e5073db331294cp165831jsn1adf94629802"  # Replace with your actual RapidAPI key
API_HOST = "youtube-mp3-audio-video-downloader.p.rapidapi.com"

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to convert video to MP3 using external API
def download_audio(video_id):
    url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download-mp3/{video_id}"
    querystring = {"quality": "high"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, stream=True)

        # Debugging logs
        st.write("Status Code:", response.status_code)
        st.write("Raw Headers:", response.headers)

        if response.status_code == 200:
            file_name = f"{video_id}.mp3"
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return file_name, None
        else:
            return None, f"HTTP Error: {response.status_code}"
    except Exception as e:
        return None, f"Request Failed: {e}"

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        # Extract the video ID from the URL
        video_id = extract_video_id(url)
        if video_id:
            # Download the audio file
            file_name, error_message = download_audio(video_id)
            if file_name:
                st.success(f"Download successful! File saved as {file_name}.")
                with open(file_name, "rb") as audio_file:
                    st.download_button(
                        label="Download MP3",
                        data=audio_file,
                        file_name=file_name,
                        mime="audio/mpeg"
                    )
            else:
                st.error(f"Error: {error_message}")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Optional: "Reset Conversion" button to clear fields
if st.button("Reset Conversion"):
    st.experimental_rerun()  # Refresh the app to reset the URL input
