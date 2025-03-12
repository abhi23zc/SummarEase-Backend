# YouTube Transcript Extractor API

This is a Flask-based API that extracts transcripts from YouTube videos using the `youtube-transcript-api`. The API supports extracting video IDs from various YouTube URL formats (both desktop and mobile) and returns the transcript in JSON format.

## Features
- Extracts video transcripts using the `youtube-transcript-api`
- Supports CORS for frontend integration
- Handles different YouTube URL formats

## Requirements
Ensure you have Python installed along with the following dependencies:

```sh
pip install flask flask-cors youtube-transcript-api
```

## Setup and Running the API
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/flask-youtube-transcript.git
   cd flask-youtube-transcript
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```sh
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000/`

## API Endpoints
### Extract YouTube Transcript
#### Request:
- **Endpoint:** `/get_transcript`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Payload:**
  ```json
  {
    "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }
  ```

#### Response:
- **Success (200):**
  ```json
  {
    "transcript": "This is the transcript of the video."
  }
  ```
- **Error (400):**
  ```json
  {
    "error": "No video ID provided"
  }
  ```
- **Error (500):**
  ```json
  {
    "error": "An error occurred while fetching the transcript"
  }
  ```

## Extracting Video ID from YouTube URL
The API extracts video IDs from different YouTube URL formats including:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## CORS Handling
The API supports CORS to allow cross-origin requests from the frontend:
```python
from flask_cors import CORS
CORS(app)
```

## Frontend Integration (Axios Example)
You can fetch the transcript using Axios in a React app:

```javascript
import axios from 'axios';

const fetchTranscript = async (videoUrl) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/get_transcript', { video_url: videoUrl });
    console.log(response.data.transcript);
  } catch (error) {
    console.error("Error fetching transcript", error);
  }
};
```

## License
This project is licensed under the MIT License.

