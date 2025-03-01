# app/routes.py
from flask import Blueprint, request, jsonify, send_from_directory
import yt_dlp
import os

# Define un Blueprint para las rutas
app_bp = Blueprint('app_bp', __name__)

@app_bp.route('/')
def index():
    return send_from_directory(app_bp.static_folder, 'index.html')

@app_bp.route('/ser1')
def ser1():
    return send_from_directory(app_bp.static_folder, 'ser1.html')

@app_bp.route('/get-media-info', methods=['POST'])
def get_media_info():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        ydl_opts = {
            'format': 'best',
            'cookiefile': '/etc/secrets/cookies.txt' if os.path.exists('/etc/secrets/cookies.txt') else None,
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