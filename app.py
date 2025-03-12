from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS  
import re
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)  


def get_transcript_text(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],  # Change language if needed
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        subtitles = info.get('subtitles', {}).get('en', [])
        
        if not subtitles:
            return "Transcript not available."

        subtitle_url = subtitles[0]['url']  # Get subtitle URL
        
        # Fetch subtitle content
        response = requests.get(subtitle_url)
        if response.status_code == 200:
            return response.text  # Returns raw transcript text
        
    return "Could not fetch transcript."



def extract_video_id(url):
    video_id = None

    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})",
        r"(?:https?:\/\/)?m\.youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/|live\/)([a-zA-Z0-9_-]{11})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break

    return video_id


def extract_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t['text'] for t in transcript])

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    print("Fetching Data")
    data = request.json
    print(data)
    
    youtube_url = data.get("video_id")
    
    if not youtube_url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = get_transcript_text(youtube_url)
        return jsonify({"video_id": video_id, "transcript": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



