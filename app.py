from flask import Flask, request, jsonify
import yt_dlp
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Use environment variable for API key (recommended)
API_KEY = "AIzaSyCMdeDSl5K0mye8ARUM1desybHdnFKa9lk"
COOKIE_FILE = 'exported_cookies.json'  # Path to your cookies file

def search_youtube(query):
    """Search for the YouTube video ID using the YouTube Data API v3."""
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' not in search_response or len(search_response['items']) == 0:
        raise ValueError('No videos found for the query.')

    video_id = search_response['items'][0]['id']['videoId']
    return video_id

@app.route('/get-audio-url', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Use YouTube API to get video ID
        video_id = search_youtube(query)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        # 'cookies': COOKIE_FILE  # Uncomment if using cookies
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
            audio_url = info['url']
            return jsonify({'url': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure to listen on 0.0.0.0 to allow external connections
    app.run(debug=True, host='0.0.0.0', port=8000)
