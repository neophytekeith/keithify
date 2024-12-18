import requests

# URL of the API that provides the audio file
url = "https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download-m4a/R1F7nAomdn8"

headers = {
    "x-rapidapi-key": "3d094d7278msh8e5073db331294cp165831jsn1adf94629802",
    "x-rapidapi-host": "youtube-mp3-audio-video-downloader.p.rapidapi.com"
}

# Send the request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    data = response.json()

    # If the API returned a valid status and a file URL
    if data.get("status") == "success":
        file_url = data.get("link")  # The URL to the audio file
        file_name = "downloaded_audio.mp3"  # You can change the name and extension to .mp3 if needed

        # Download the file from the URL
        file_response = requests.get(file_url)

        # If the file was successfully downloaded
        if file_response.status_code == 200:
            # Open the file in binary write mode and save it
            with open(file_name, 'wb') as f:
                f.write(file_response.content)
            print(f"Audio file saved as {file_name}")
        else:
            print(f"Failed to download the file. Status code: {file_response.status_code}")
    else:
        print(f"Error: {data.get('msg')}")
else:
    print(f"HTTP Error: {response.status_code}")
