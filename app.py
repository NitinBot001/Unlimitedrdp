from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-audio-url', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Use yt-dlp with cookies JSON to fetch the audio URL
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch',
            'cookiefile': 'exported-cookies.json',  # Path to your cookies JSON file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]  # If a search query returns multiple results, use the first
            audio_url = info_dict['url']

        return jsonify({'url': audio_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
