from flask import Flask, request, jsonify
import pafy
import yt_dlp
from googleapiclient.discovery import build

# Set yt-dlp as the backend for pafy
pafy.set_backend("yt-dlp")

# Your YouTube API key
API_KEY = "AIzaSyCMdeDSl5K0mye8ARUM1desybHdnFKa9lk"

app = Flask(__name__)

# Function to search YouTube using the API
def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part="id,snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']['videoId']
    return None

@app.route('/get-audio-url', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Use the YouTube API to search for the video ID
        video_id = search_youtube(query)
        if not video_id:
            return jsonify({'error': 'No video found for the given query'}), 404

        # Create a Pafy object using the video ID
        video = pafy.new(video_id)
        
        # Get the best audio stream URL
        bestaudio = video.getbestaudio()
        audio_url = bestaudio.url
        
        return jsonify({'url': audio_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
