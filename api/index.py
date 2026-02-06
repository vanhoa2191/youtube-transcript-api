from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel
import re

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.post("/transcript")
@app.post("/api/transcript")
async def get_transcript(request: VideoRequest):
    video_id = extract_video_id(request.video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['vi', 'en'])
        transcript_text = ' '.join([t['text'] for t in transcript_list])
        return {
            "video_url": request.video_url,
            "transcript": transcript_text
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No transcript available: {str(e)}")

@app.get("/")
@app.get("/api")
async def root():
    return {"status": "YouTube Transcript API is running"}
