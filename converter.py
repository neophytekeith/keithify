import os
import yt_dlp
import streamlit as st
import subprocess
from streamlit.components.v1 import html

# Set up the download directory
download_dir = "/tmp"
os.makedirs(download_dir, exist_ok=True)

# Function to clear temporary files
def clear_temp_files():
    temp_audio_file = os.path.join(download_dir, 'temp_audio.webm')
    temp_mp3_file = os.path.join(download_dir, 'temp_audio.mp3')
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)
    if os.path.exists(temp_mp3_file):
        os.remove(temp_mp3_file)

# Function to download and convert YouTube video to MP3
def download_and_convert_to_mp3(url, cookies=None):
    try:
        clear_temp_files()

        # Set up yt-dlp options with cookies if provided
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, 'temp_audio.%(ext)s'),
            'quiet': True,
            'extractaudio': True,
            'audioquality': 0,  # Ensure best quality audio
            'noplaylist': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
        }

        if cookies:
            ydl_opts['cookies'] = cookies  # Add cookies if provided

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info, including the title
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            st.write(f"Converting '{video_title}' to MP3. Please wait...")
            
            # Download the audio file
            ydl.download([url])

        # After downloading, check if the file exists
        audio_file = os.path.join(download_dir, 'temp_audio.webm')  # Expected download format
        if not os.path.exists(audio_file):
            st.error(f"Error: The downloaded file {audio_file} was not found.")
            return

        # Convert to MP3 (without re-encoding, keeping the best bitrate)
        output_mp3 = os.path.join(download_dir, f'{video_title}.mp3')
        command = ['ffmpeg', '-i', audio_file, '-vn', '-acodec', 'copy', output_mp3]
        subprocess.run(command, check=True)

        # Display success message and audio player
        st.success("Conversion successful! You can download your file below:")
        with open(output_mp3, "rb") as f:
            st.download_button(label="Download MP3", data=f, file_name=f'{video_title}.mp3', mime="audio/mp3")
        
        # Clear temporary files after conversion
        clear_temp_files()

    except Exception as e:
        st.error(f"An error occurred: {e}")

# JavaScript to extract cookies
cookie_js = """
    <script>
    function getCookies() {
        return document.cookie;
    }

    function sendCookiesToStreamlit(cookies) {
        console.log("Sending cookies to Streamlit:", cookies);  // Debugging line
        window.parent.postMessage({ type: 'cookies', cookies: cookies }, '*');
    }

    window.addEventListener('load', function() {
        const acceptButton = document.getElementById("accept-cookies");
        acceptButton.addEventListener("click", function() {
            const cookies = getCookies();
            console.log("Cookies retrieved:", cookies);  // Debugging line
            sendCookiesToStreamlit(cookies);
            document.getElementById('cookie-popup').style.display = 'none';
        });
    });
    </script>
"""

# Streamlit UI for Cookie Consent Popup
html(f"""
    <div id="cookie-popup" style="position: fixed; bottom: 20px; left: 20px; background-color: #fff; border: 1px solid #ccc; padding: 10px; z-index: 1000;">
        <p>This website uses cookies. By accepting, you agree to use your browser cookies for authentication.</p>
        <button id="accept-cookies">Accept Cookies</button>
    </div>
    {cookie_js}
""", height=200)

# Streamlit UI to input YouTube URL
st.title("YouTube to MP3 Converter")
url = st.text_input("Enter YouTube URL:")

# Variable to store cookies
cookies = None

# Listen for cookies sent from JavaScript
if st.session_state.get('cookies', None):
    cookies = st.session_state['cookies']
    st.write(f"Cookies received: {cookies}")

# Use the cookies to authenticate and download
if st.button("Download and Convert"):
    if url:
        download_and_convert_to_mp3(url, cookies)
    else:
        st.warning("Please enter a valid YouTube URL.")

# "Reset Conversion" button to reset URL and session state
if st.button("Reset Conversion"):
    cookies = None  # Reset cookies
    st.experimental_rerun()  # Refresh the app to reset everything
