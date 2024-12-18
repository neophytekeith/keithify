import streamlit as st
import requests
import re

# Set your RapidAPI credentials
API_KEY = "3d094d7278msh8e5073db331294cp165831jsn1adf94629802"  # Replace with your actual RapidAPI key
API_HOST = "youtube-mp3-audio-video-downloader.p.rapidapi.com"

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    # Try to match either of the common YouTube URL formats
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to call the RapidAPI endpoint and download the MP3
def convert_to_mp3(video_id):
    url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download-mp3/{video_id}"
    querystring = {"quality": "low"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        # Send the API request
        response = requests.get(url, headers=headers, params=querystring)

        # Check the HTTP status code and raw response
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            if data.get("status") == "ok":
                download_link = data.get("link")
                song_title = data.get("title")

                # Download the MP3 file
                mp3_response = requests.get(download_link)
                if mp3_response.status_code == 200:
                    file_name = f"{song_title}.mp3"
                    with open(file_name, "wb") as file:
                        file.write(mp3_response.content)
                    return file_name, f"Download successful! File saved as {file_name}."
                else:
                    return None, f"Failed to download MP3. HTTP Status: {mp3_response.status_code}"
            else:
                return None, f"API Error: {data.get('msg', 'Unknown error')}"
        else:
            return None, f"HTTP Error: {response.status_code}. Check the raw response for details."
    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {e}"

# Streamlit UI
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        # Extract the video ID from the URL
        video_id = extract_video_id(url)
        if video_id:
            # Convert the video to MP3
            file_name, message = convert_to_mp3(video_id)
            if file_name:
                st.success(message)
                st.markdown(f"[Download your MP3 file](./{file_name})")
            else:
                st.error(message)
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Optional: Reset conversion
if st.button("Reset Conversion"):
    st.experimental_rerun()
