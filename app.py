from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# Define a function to extract video metadata and audio streaming URL using yt-dlp
def get_video_metadata_and_audio_url(search_query, username=None, password=None):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best',  # Ensure we are fetching the best audio stream
        'extract_flat': False  # We want the actual stream URL, not just metadata
    }

    # Add login credentials if provided
    if username and password:
        ydl_opts.update({
            'username': username,
            'password': password
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Use yt-dlp to search and get metadata, including streaming URLs
            result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            
            if 'entries' in result:
                # Extract metadata and audio URL of the first search result
                video = result['entries'][0]
                audio_url = video.get('url')  # Direct audio streaming URL
                
                # Return metadata along with the audio streaming URL
                return {
                    'title': video.get('title'),
                    'id': video.get('id'),
                    'url': video.get('webpage_url'),
                    'duration': video.get('duration'),
                    'uploader': video.get('uploader'),
                    'view_count': video.get('view_count'),
                    'like_count': video.get('like_count'),
                    'description': video.get('description'),
                    'audio_stream_url': audio_url  # Adding the actual audio stream URL
                }
            else:
                return {'error': 'No videos found'}

        except Exception as e:
            return {'error': str(e)}

# Define a route for video search and metadata fetching
@app.route('/search', methods=['GET'])
def search_video():
    query = request.args.get('query')
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    # Get video metadata and audio streaming URL
    metadata = get_video_metadata_and_audio_url(query, username, password)
    return jsonify(metadata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
