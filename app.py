from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# Path to your cookies file
COOKIES_FILE = 'cookies.txt'

def get_video_url(query):
    ydl_opts = {
        'cookies': COOKIES_FILE,
        'quiet': True,
        'force_generic_extractor': True,
        'noplaylist': True,
        'default_search': 'ytsearch',
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            video_url = info['formats'][0]['url']  # Direct stream URL
            return video_url
        except Exception as e:
            return str(e)

@app.route('/get_video_url', methods=['GET'])
def get_video_url_route():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    video_url = get_video_url(query)
    return jsonify({'url': video_url})

if __name__ == '__main__':
    app.run(debug=True)
