import os
from pathlib import Path
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

class AudioTranscriber:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided")
        aai.settings.api_key = self.api_key

    def transcribe(self, audio_source: str) -> str:
        """
        Transcribe audio from file path or URL.

        Args:
            audio_source: Local file path or URL to audio file

        Returns:
            Transcription text
        """
        transcript = aai.Transcriber().transcribe(audio_source)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        return transcript.text

    def transcribe_with_details(self, audio_source: str) -> dict:
        """
        Transcribe audio and return detailed information.

        Returns:
            Dictionary with text, status, and other metadata
        """
        transcript = aai.Transcriber().transcribe(audio_source)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        return {
            "text": transcript.text,
            "status": transcript.status,
            "id": transcript.id,
            "audio_duration": transcript.audio_duration
        }
