import requests

# Apify API URL for the YouTube video and MP3 downloader actor
url = "https://api.apify.com/v2/acts/easyapi~youtube-video-and-mp3-downloader/run-sync-get-dataset-items"

# Define the query parameters (you can change the video URL here)
querystring = {
    "token": "apify_api_AWbTlHovmyHtiHrhFy28LRtVHzRzP60pHwiq",  # Replace with your Apify API token
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Replace with your YouTube video URL
}

# Sending GET request to the Apify API endpoint
response = requests.get(url, params=querystring)

# Check if the response is successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Check if the 'data' field is in the response
    if 'data' in data:
        # Iterate through each item in the 'data' list
        for item in data['data']:
            # Extract and print the relevant details
            title = item.get('title', 'No title available')
            download_url = item.get('downloadUrl', 'No download URL available')
            status = item.get('status', 'Status not available')
            print(f"Downloading {title} as MP3. Please wait...")
            print(f"Title: {title}")
            print(f"Download URL: {download_url}")
            print(f"Status: {status}")
    else:
        print("No data found in the response.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
