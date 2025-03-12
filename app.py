from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS  
import re
import requests

app = Flask(__name__)
CORS(app)  

# ScraperAPI key (Replace with your actual API key)
SCRAPER_API_KEY = "b2cd891913a261a35c4b577b1b74524a"

# Function to extract video ID from any YouTube URL
def extract_video_id(url):
    video_id = None
    
    # Regular expressions for different YouTube URL formats
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

# Function to extract transcript using ScraperAPI
def extract_transcript(video_id):
    # ScraperAPI URL
    scraper_url = f"https://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url=https://www.youtube.com/watch?v={video_id}"

    try:
        # Fetch transcript using ScraperAPI proxy
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": scraper_url, "https": scraper_url})
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        return str(e)

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
        transcript = extract_transcript(video_id)
        return jsonify({"video_id": video_id, "transcript": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
