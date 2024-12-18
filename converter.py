import os
import yt_dlp
import streamlit as st
import subprocess

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
def download_and_convert_to_mp3(url):
    try:
        clear_temp_files()

        # Set up yt-dlp options without cookies
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

# Check if the user has already consented to cookies using Streamlit session state
if 'cookie_consent' not in st.session_state:
    # Display cookie consent message
    st.markdown("""
        <div style="background-color: #f1f1f1; padding: 10px; border-radius: 5px; text-align: center;">
            <strong>This website uses cookies to improve your experience.</strong>
            <br><br>
            By clicking "Accept", you agree to our use of cookies. 
            <br><br>
        </div>
        """, unsafe_allow_html=True)

    # Button to accept cookies
    if st.button("Accept Cookies"):
        st.session_state.cookie_consent = True  # Store the consent in session state
        st.write("Thank you for accepting the cookies!")
else:
    # Content to display after the user accepts cookies
    st.write("Welcome back! You have already accepted the cookies.")

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")
if 'url' not in st.session_state:
    st.session_state.url = ""

url = st.text_input("Enter YouTube URL:", key="url")
if st.button("Download and Convert"):
    if url:
        download_and_convert_to_mp3(url)
    else:
        st.warning("Please enter a valid YouTube URL.")

# "Reset Conversion" button to reset URL and session state
if st.button("Reset Conversion"):
    st.session_state.url = ""  # This will reset the input field
    clear_temp_files()  # Clear the temporary files
    st.experimental_rerun()  # Refresh the app to reset the URL input
