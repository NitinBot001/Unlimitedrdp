from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

def is_youtube_url(url):
    """Check if the provided URL starts with YouTube URL prefixes."""
    return url.startswith('https://www.youtube.com/watch?v=') or url.startswith('https://youtu.be/')

@app.route('/get-audio-url', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        if is_youtube_url(query):
            video_url = query
        else:
            # Construct a search URL if it's not a direct YouTube URL
            video_url = f'https://www.youtube.com/results?search_query={query}'

        # Fetch video details
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not audio_stream:
            return jsonify({'error': 'No audio stream available'}), 404
        audio_url = audio_stream.url

        return jsonify({'url': audio_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
