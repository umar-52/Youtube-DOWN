import os
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

# Temporary folder jahan file pehle save hogi
TEMP_DIR = 'downloads_temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_preview', methods=['POST'])
def get_preview():
    url = request.json.get('url')
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            return jsonify({
                'title': info.get('title'),
                'embed_url': f"https://www.youtube.com/embed/{video_id}"
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    try:
        # File ko server par download karna
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
        # File ko Phone/PC ke browser mein bhejna
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' taaki mobile par chale
    app.run(host='0.0.0.0', port=5000, debug=True)
