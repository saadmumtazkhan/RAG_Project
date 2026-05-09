from youtube_transcript_api import YouTubeTranscriptApi
from app.config import VIDEO_ID


def fetch_transcript():

    api = YouTubeTranscriptApi()

    fetched_transcript = api.fetch(
        VIDEO_ID,
        languages=["en"]
    )

    transcript = []

    for snippet in fetched_transcript:
        transcript.append({
            "text": snippet.text,
            "start": snippet.start,
            "duration": snippet.duration
        })

    print(f"Fetched {len(transcript)} transcript segments")

    return transcript


def transcript_to_text(transcript):

    return " ".join(
        [segment["text"] for segment in transcript]
    )
