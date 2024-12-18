import requests
import time

# YouTube video URL and format choice
video_url = "https://www.youtube.com/watch?v=zyG9Nh_PH38"  # Replace with actual URL
quality = "high"  # or low, medium, etc.

# API URL and headers
url = "https://youtube-to-mp315.p.rapidapi.com/download"
querystring = {"url": video_url, "format": "mp3"}
headers = {
    "x-rapidapi-key": "3d094d7278msh8e5073db331294cp165831jsn1adf94629802",  # Replace with your API key
    "x-rapidapi-host": "youtube-to-mp315.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Start the download request
response = requests.post(url, headers=headers, params=querystring)

# Check if the response was successful
if response.status_code == 200:
    data = response.json()
    status = data.get('status')

    if status == "CONVERTING":
        print("The file is currently being converted. Please wait...")

        # Implement a check to repeatedly request the status until the file is ready for download
        while status == "CONVERTING":
            # You may want to add a delay to avoid overwhelming the API with requests
            time.sleep(5)  # Wait 5 seconds before checking again

            # Re-query the status endpoint to get updated information
            status_url = f"https://youtube-to-mp315.p.rapidapi.com/status/{data['id']}"
            status_response = requests.get(status_url, headers=headers)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get('status')
                print(f"Current status: {status}")
            else:
                print("Error fetching status information.")
                break

        # Once the status is no longer "CONVERTING", check if the file is available
        if status == "AVAILABLE":
            download_url = data['downloadUrl']
            print(f"The MP3 file is ready for download! Download it from: {download_url}")
        else:
            print("Error: Conversion failed or timed out.")

    else:
        print(f"Error: {status}. File is not being converted.")
else:
    print(f"Error: Failed to initiate download. HTTP Status Code: {response.status_code}")
