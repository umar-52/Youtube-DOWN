import os
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__, template_folder='templates')

# Temporary folder jahan file pehle save hogi
TEMP_DIR = 'downloads_temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_preview', methods=['POST'])
def get_preview():
    data = request.json
    url = data.get('url')
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # Ye YouTube ko pagal banane ke liye hai
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'extract_flat': True,
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            # Agar YouTube hai toh embed link, warna thumbnail
            if 'youtube' in url or 'youtu.be' in url:
                preview_url = f"https://www.youtube.com/embed/{video_id}"
            else:
                preview_url = info.get('thumbnail')
                
            return jsonify({
                'embed_url': preview_url,
                'title': info.get('title')
            })
    except Exception as e:
        # Agar phir bhi block kare, toh ye dummy link bhej dega taaki button na fase
        return jsonify({'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'title': 'Checking Server...'}), 200
    # Instagram ya dusri sites ke liye thumbnail dikha do
    embed_url = info.get('thumbnail') 

return jsonify({
    'embed_url': embed_url,
    'title': info.get('title')
})

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        # Ye niche wali lines YouTube block se bachati hain
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            return jsonify({
                'embed_url': f"https://www.youtube.com/embed/{video_id}",
                'title': info.get('title')
            })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
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
