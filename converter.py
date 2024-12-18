import streamlit as st
from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_AWbTlHovmyHtiHrhFy28LRtVHzRzP60pHwiq")  # Using your actual API token

# Streamlit app header
st.title('YouTube to MP3 Converter')
st.write('Enter a YouTube video URL below to convert it to MP3.')

# Input field for YouTube URL
youtube_url = st.text_input('Enter YouTube URL:', '')

# Convert button
if st.button('Convert to MP3'):
    if youtube_url:
        st.write(f"Converting {youtube_url}... Please wait.")

        # Prepare the input for the Apify actor (pass the entered YouTube URL)
        run_input = {
            "links": [youtube_url]
        }

        try:
            # Run the Actor and wait for it to finish
            run = client.actor("jvDjDIPtCZAcZo9jb").call(run_input=run_input)

            # Fetch and display the result from the dataset
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                # Displaying information to the user
                if item.get("status") == "AVAILABLE":
                    st.success(f"Download {item['title']} in MP3 format!")
                    st.audio(item["downloadUrl"], format="audio/mp3", start_time=0)
                    st.write(f"Title: {item.get('title')}")
                    st.write(f"Download URL: [Click here]({item.get('downloadUrl')})")
                elif item.get("status") == "CONVERTING":
                    st.warning(f"Your video '{item.get('title')}' is still being converted. Please wait a moment.")
                else:
                    st.error("There was an issue with the conversion. Please try again later.")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning('Please enter a YouTube URL to start the conversion.')

