import logging
import io
from openai import OpenAI


client = OpenAI()

class AIClient:

    @classmethod
    def transcribe_audio(cls, audio_data, key: str) -> str:
        try:
            audio_file = io.BytesIO(audio_data)
            audio_file.name = key.split('/')[-1]

            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
            return transcript.text
        except Exception as e:
            raise RuntimeError(f"Audio transcription failed: {e}")