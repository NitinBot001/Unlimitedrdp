from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/get-audio-url', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            audio_url = info['url']
            return jsonify({'url': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default port is 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
