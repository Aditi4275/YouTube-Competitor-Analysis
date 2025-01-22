from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=API_KEY)

if not API_KEY:
    raise ValueError("YouTube API Key not found. Please set YOUTUBE_API_KEY in the .env file.")

def search_channels_by_niche(niche, max_results=20):
    # Step 1: Search for channels by niche
    search_request = youtube.search().list(
        q=niche,
        part='snippet',
        type='channel',
        maxResults=max_results
    )
    search_response = search_request.execute()

    # Step 2: Extract channel IDs
    channel_ids = [item['snippet']['channelId'] for item in search_response.get('items', [])]

    # Step 3: Fetch channel statistics in a single API call
    stats_request = youtube.channels().list(
        part='snippet,statistics',
        id=','.join(channel_ids)  # Fetch details for all channels at once
    )
    stats_response = stats_request.execute()

    # Step 4: Format the data into a DataFrame
    channels = []
    for item in stats_response.get('items', []):
        channels.append({
            'channel_id': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'subscribers': int(item['statistics'].get('subscriberCount', 0)),
            'video_count': int(item['statistics'].get('videoCount', 0)),
            'view_count': int(item['statistics'].get('viewCount', 0)),
        })

    # Step 5: Convert to DataFrame
    df = pd.DataFrame(channels)
    return df