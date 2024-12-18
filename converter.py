import streamlit as st
import requests
import re

# Define the API keys and URLs for the three endpoints
API_KEY = "3d094d7278msh8e5073db331294cp165831jsn1adf94629802"
API_HOST = "youtube-to-mp315.p.rapidapi.com"

# Extract the YouTube video ID from the URL
def extract_video_id(url):
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to fetch video title using the title endpoint
def get_video_title(video_id):
    url = f"https://youtube-to-mp315.p.rapidapi.com/title"
    querystring = {"url": f"https://www.youtube.com/watch?v={video_id}"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            return data.get("title", "No title available")
        else:
            return None
    except Exception as e:
        return None

# Function to check the conversion status
def check_conversion_status(conversion_id):
    url = f"https://youtube-to-mp315.p.rapidapi.com/status/{conversion_id}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "Unknown status")
            download_url = data.get("downloadUrl", None)
            if status == "AVAILABLE" and download_url:
                return status, download_url
            else:
                return status, None
        else:
            return None, None
    except Exception as e:
        return None, None

# Function to download the MP3
def download_mp3(video_id):
    url = "https://youtube-to-mp315.p.rapidapi.com.download"
    querystring = {"url": f"https://www.youtube.com/watch?v={video_id}", "format": "mp3"}
    payload = {}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            conversion_id = data.get("id", None)
            if conversion_id:
                return conversion_id
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

# Streamlit UI
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Get Video Title"):
    if url:
        video_id = extract_video_id(url)
        if video_id:
            title = get_video_title(video_id)
            if title:
                st.success(f"Video Title: {title}")
            else:
                st.error("Error: Could not fetch the title.")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a YouTube URL.")

if st.button("Download MP3"):
    if url:
        video_id = extract_video_id(url)
        if video_id:
            # First, initiate the download process
            conversion_id = download_mp3(video_id)
            if conversion_id:
                # Check the conversion status
                status, download_url = check_conversion_status(conversion_id)
                if status == "AVAILABLE" and download_url:
                    st.success("Download MP3:")
                    st.markdown(f"[Download MP3]({download_url})")
                else:
                    st.error(f"Conversion Status: {status}")
            else:
                st.error("Error: Could not initiate the download process.")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a YouTube URL.")
