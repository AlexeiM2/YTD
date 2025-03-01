from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/ser1')
def ser1():
    return send_from_directory(app.static_folder, 'ser1.html')

@app.route('/get-media-info', methods=['POST'])
def get_media_info():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        ydl_opts = {
            'format': 'best',
            'cookiefile': '/etc/secrets/cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except yt_dlp.utils.DownloadError as e:
                if "Sign in to confirm" in str(e):
                    return jsonify({'error': 'Autenticación requerida'}), 401
                elif "Video unavailable" in str(e):
                    return jsonify({'error': 'Video no disponible'}), 404
                raise e

        audio_url = None
        video_url = None
        for f in info.get('formats', []):
            if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                audio_url = f['url']
            elif f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                video_url = f['url']

        return jsonify({
            'title': info.get('title'),
            'audio_url': audio_url,
            'video_url': video_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)