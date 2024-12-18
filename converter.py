import streamlit as st
import requests
import re

# Set your RapidAPI credentials
API_KEY = "3d094d7278msh8e5073db331294cp165831jsn1adf94629802"  # Replace with your actual RapidAPI key
API_HOST = "youtube-mp3-audio-video-downloader.p.rapidapi.com"

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    else:
        video_id = None
    return video_id.group(1) if video_id else None

# Function to fetch video title
def fetch_video_title(video_id):
    url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/video-info/{video_id}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("title", "Unknown Title")
        else:
            return None
    except Exception as e:
        return None

# Function to download audio
def download_audio(video_id):
    url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download-mp3/{video_id}"
    querystring = {"quality": "high"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, stream=True)
        if response.status_code == 200:
            # Extract file name from the response headers
            file_name = response.headers.get("Content-Disposition", "audio.mp3").split("filename=")[-1].strip('"')
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return file_name, None
        elif response.status_code == 404:
            return None, "Error: Resource not found (404). Check the video ID or endpoint."
        else:
            return None, f"HTTP Error: {response.status_code}"
    except Exception as e:
        return None, f"Request Failed: {e}"

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        video_id = extract_video_id(url)
        if video_id:
            # Fetch video title
            video_title = fetch_video_title(video_id)
            if video_title:
                st.info(f"Downloading **{video_title}** as MP3. Please wait...")
            else:
                st.warning("Unable to fetch video title. Proceeding with download...")

            # Download the audio file
            file_name, error_message = download_audio(video_id)
            if file_name:
                st.success(f"Download successful! File saved as {file_name}.")
                with open(file_name, "rb") as audio_file:
                    st.download_button(
                        label="Download MP3",
                        data=audio_file,
                        file_name=file_name,
                        mime="audio/mpeg",
                    )
            else:
                st.error(error_message)
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a YouTube URL.")

# Optional: Reset the app
if st.button("Reset Conversion"):
    st.experimental_rerun()
