"""Transcription service using Whisper API"""

import requests
from typing import Optional, List, Dict
from app.config import settings
from app.models.transcript import TranscriptSegment
import json


class TranscriptionService:
    """Transcription service using OpenAI Whisper"""

    def __init__(self):
        self.api_key = settings.WHISPER_API_KEY
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"

    async def transcribe_file(
        self,
        file_path: str,
        language: str = "vi",
    ) -> Dict:
        """Transcribe audio file using Whisper API"""

        if not self.api_key:
            # Return mock data for development
            return self._get_mock_transcript()

        try:
            with open(file_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {
                    "model": "whisper-1",
                    "language": language,
                    "response_format": "verbose_json",
                }
                headers = {"Authorization": f"Bearer {self.api_key}"}

                response = requests.post(
                    self.api_url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=300,
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(
                        f"Whisper API error: {response.status_code} - {response.text}"
                    )

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    def parse_whisper_response(self, whisper_data: Dict) -> Dict:
        """Parse Whisper API response into our format"""

        segments = []

        if "segments" in whisper_data:
            for seg in whisper_data["segments"]:
                segments.append({
                    "start_time": seg.get("start", 0),
                    "end_time": seg.get("end", 0),
                    "text": seg.get("text", ""),
                    "speaker": None,
                    "confidence": seg.get("confidence", 0.9),
                })

        return {
            "content": whisper_data.get("text", ""),
            "segments": segments,
            "language": whisper_data.get("language", "vi"),
            "duration": whisper_data.get("duration", 0),
        }

    def detect_silence(
        self,
        segments: List[Dict],
        min_silence_duration: float = 2.0,
    ) -> List[Dict]:
        """Detect silence periods from transcript segments"""

        if not segments or len(segments) == 0:
            return []

        silence_segments = []
        segments = sorted(segments, key=lambda x: x["start_time"])

        # Check gaps between segments
        for i in range(len(segments) - 1):
            gap_start = segments[i]["end_time"]
            gap_end = segments[i + 1]["start_time"]
            gap_duration = gap_end - gap_start

            if gap_duration >= min_silence_duration:
                silence_segments.append({
                    "start_time": gap_start,
                    "end_time": gap_end,
                    "duration": gap_duration,
                })

        return silence_segments

    def _get_mock_transcript(self) -> Dict:
        """Return mock transcript for development (no API key)"""
        return {
            "text": "Xin chào, đây là bản ghi âm mẫu cho phát triển. Hệ thống đang hoạt động tốt.",
            "language": "vi",
            "duration": 10.0,
            "segments": [
                {
                    "id": 0,
                    "seek": 0,
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Xin chào, đây là bản ghi âm mẫu cho phát triển.",
                    "tokens": [],
                    "temperature": 0.0,
                    "avg_logprob": -0.3,
                    "compression_ratio": 1.2,
                    "no_speech_prob": 0.001,
                    "confidence": 0.95,
                },
                {
                    "id": 1,
                    "seek": 0,
                    "start": 5.0,
                    "end": 10.0,
                    "text": "Hệ thống đang hoạt động tốt.",
                    "tokens": [],
                    "temperature": 0.0,
                    "avg_logprob": -0.25,
                    "compression_ratio": 1.1,
                    "no_speech_prob": 0.002,
                    "confidence": 0.92,
                },
            ],
        }


# Singleton instance
transcription_service = TranscriptionService()
