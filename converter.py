import streamlit as st
import requests
import re

# Set your API key and host URL for Vevioz API
API_BASE_URL = "https://api.vevioz.com/@api/button/mp3"  # This endpoint is for MP3 conversion

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to get the conversion link
def get_conversion_link(video_id):
    url = f"https://api.vevioz.com/@api/button/mp3/{video_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Assuming the response is the mp3 download link
            data = response.json()
            return data['link']
        else:
            return None
    except Exception as e:
        return None

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3/MP4 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        # Extract the video ID from the URL
        video_id = extract_video_id(url)
        if video_id:
            # Fetch conversion link
            download_link = get_conversion_link(video_id)
            if download_link:
                st.success(f"Download the MP3 from the link below:")
                st.markdown(f"[Download MP3]({download_link})")
            else:
                st.error("Error: Could not get conversion link.")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a YouTube URL.")

# Optional: "Reset Conversion" button to clear fields
if st.button("Reset Conversion"):
    st.experimental_rerun()  # Refresh the app to reset the URL input
