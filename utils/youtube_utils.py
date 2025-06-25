import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_video_title(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"

    class SilentLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): pass

    options = {
        'quiet': True,
        'no_warnings': True,
        'logger': SilentLogger(),
        'skip_download': True
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['title']
    except Exception as e:
        return f"Video ID: {video_id}"

    
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", url)
    return match.group(1) if match else None

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([seg["text"] for seg in transcript])