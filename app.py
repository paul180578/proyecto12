from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Por favor, ingresa un enlace de YouTube.", 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',  
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            video_title = result.get('title', None)
            video_file = f"{video_title}.mp4"

        # Convertir el video descargado a MP3
        audio = AudioFileClip(video_file)
        mp3_file = f"{video_title}.mp3"
        audio.write_audiofile(mp3_file)
        audio.close()

        # Eliminar el archivo MP4 original
        os.remove(video_file)

        # Enviar el archivo MP3 al usuario
        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return f"Ocurrió un error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
