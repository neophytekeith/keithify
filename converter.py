import streamlit as st
import http.client
import json
import re

# Set your API key and host URL
API_KEY = "d90a09a015msh12f69eb58ce9364p149b89jsnd92118bd82d3"  # Replace with your actual RapidAPI key
API_HOST = "youtube-mp3-download3.p.rapidapi.com"

# Function to extract YouTube video ID from the URL
def extract_video_id(url):
    # Try to match either of the common YouTube URL formats
    video_id = None
    if "youtu.be" in url:
        video_id = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    elif "youtube.com" in url:
        video_id = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", url)
    return video_id.group(1) if video_id else None

# Function to convert video to MP3 using the external API (via custom HTTP client)
def convert_to_mp3(video_url):
    # Encoding the URL
    encoded_url = video_url.replace("https://", "%3A%2F%2F").replace("/", "%2F").replace("?", "%3F").replace("=", "%3D").replace("&", "%26")
    
    # Setting up the connection to the RapidAPI
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    # Constructing the API request URL
    request_url = f"/downloads/convert_audio?url={encoded_url}&format=mp3"

    # Sending GET request to the API
    conn.request("GET", request_url, headers=headers)

    # Getting the response
    res = conn.getresponse()

    # Check if the request was successful
    if res.status == 200:
        # Reading and decoding the response data
        data = res.read()
        response = json.loads(data.decode("utf-8"))  # Parse JSON response

        # Checking the response status
        if response.get('status') == 'ok':
            song_title = response.get('title')
            download_link = response.get('link')
            conn.close()  # Close the connection
            return song_title, download_link
        else:
            conn.close()
            return None, response.get('msg', 'Unknown error occurred')
    else:
        conn.close()
        return None, f"Error: Failed to fetch data. HTTP Status Code: {res.status}"

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")

url = st.text_input("Enter YouTube URL:")

if st.button("Convert to MP3"):
    if url:
        # Extract the video ID from the URL
        video_id = extract_video_id(url)
        if video_id:
            # Construct full video URL
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            # Call the external API to convert video to MP3
            song_title, download_link = convert_to_mp3(video_url)
            if song_title:
                st.success(f"Conversion successful! You can download the MP3 below.")
                st.write(f"Song Title: {song_title}")
                st.markdown(f"[Download MP3]({download_link})")
            else:
                st.error(f"Error: {download_link}")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Optional: "Reset Conversion" button to clear fields
if st.button("Reset Conversion"):
    st.experimental_rerun()  # Refresh the app to reset the URL input
