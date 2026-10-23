"""Auto Studio AI service - automatic video generation"""

from typing import List, Dict, Any, Optional
from app.models.transcript import TranscriptSegment
import json


class AutoStudioService:
    """Automatic video studio generation"""

    @staticmethod
    def analyze_content(segments: List[Dict], transcript_text: str) -> Dict[str, Any]:
        """Analyze content for highlights and structure"""

        highlights = []
        key_phrases = []

        # Find highlight segments (longer speaking, important words)
        important_words = [
            'quan trọng', 'chính yếu', 'cần chú ý', 'đặc biệt',
            'cảnh báo', 'tuyệt vời', 'thành công', 'hiệu quả',
            'chứng minh', 'kết quả', 'tác dụng', 'công dụng'
        ]

        for i, seg in enumerate(segments):
            text = seg.get('text', '').lower()
            duration = seg.get('end_time', 0) - seg.get('start_time', 0)

            # Check if segment contains important keywords
            has_important = any(word in text for word in important_words)

            # Highlight criteria: >3s duration OR contains important words
            if (duration > 3.0) or has_important:
                highlight = {
                    'start_time': seg.get('start_time', 0),
                    'end_time': seg.get('end_time', 0),
                    'duration': duration,
                    'text': seg.get('text', ''),
                    'importance': 'high' if has_important else 'medium',
                    'type': 'speech',
                }
                highlights.append(highlight)

                # Extract key phrases
                if has_important:
                    words = text.split()
                    for word in important_words:
                        if word in text:
                            key_phrases.append(word)

        return {
            'highlights': highlights,
            'key_phrases': list(set(key_phrases)),
            'total_highlights': len(highlights),
        }

    @staticmethod
    def suggest_structure(
        duration: float,
        highlights: List[Dict],
        silence_segments: List[Dict],
    ) -> Dict[str, Any]:
        """Suggest video structure (intro, body, outro)"""

        # Calculate segments
        intro_duration = min(5.0, duration * 0.1)
        outro_duration = min(3.0, duration * 0.05)
        body_duration = duration - intro_duration - outro_duration

        # Find best highlights for body
        sorted_highlights = sorted(
            highlights,
            key=lambda x: 1.0 if x.get('importance') == 'high' else 0.5,
            reverse=True
        )[:5]  # Top 5

        return {
            'intro': {
                'duration': intro_duration,
                'type': 'text_overlay',
                'content': 'Chào mừng',
            },
            'body': {
                'duration': body_duration,
                'type': 'highlight_sequence',
                'highlights': sorted_highlights,
                'total_cuts': len(sorted_highlights),
            },
            'outro': {
                'duration': outro_duration,
                'type': 'text_overlay',
                'content': 'Cảm ơn các bạn',
            },
        }

    @staticmethod
    def generate_auto_cuts(
        segments: List[Dict],
        silence_segments: List[Dict],
        min_silence_duration: float = 1.5,
    ) -> List[Dict]:
        """Generate automatic cuts based on silence and pacing"""

        cuts = []

        # Natural break points (silence + long segments)
        for silence in silence_segments:
            if silence.get('duration', 0) >= min_silence_duration:
                cuts.append({
                    'type': 'silence_cut',
                    'start_time': silence.get('start_time', 0),
                    'end_time': silence.get('end_time', 0),
                    'duration': silence.get('duration', 0),
                    'reason': 'Khoảng lặng dài',
                })

        # Combine consecutive segments for better pacing
        return sorted(cuts, key=lambda x: x.get('start_time', 0))

    @staticmethod
    def generate_draft_timeline(
        media_id: str,
        segments: List[Dict],
        highlights: List[Dict],
        structure: Dict,
        silence_segments: List[Dict],
    ) -> Dict[str, Any]:
        """Generate draft timeline structure"""

        clips = []
        current_time = 0.0

        # Add intro
        intro = structure.get('intro', {})
        if intro.get('duration', 0) > 0:
            clips.append({
                'id': 'intro-0',
                'type': 'text',
                'start_time': current_time,
                'duration': intro.get('duration', 3.0),
                'content': intro.get('content', ''),
            })
            current_time += intro.get('duration', 3.0)

        # Add body - highlight sequences
        body = structure.get('body', {})
        for i, highlight in enumerate(body.get('highlights', [])[:5]):
            clip = {
                'id': f'clip-{i}',
                'type': 'video',
                'media_id': media_id,
                'original_start': highlight.get('start_time', 0),
                'original_duration': highlight.get('duration', 0),
                'timeline_start': current_time,
                'duration': highlight.get('duration', 0),
                'importance': highlight.get('importance', 'medium'),
            }
            clips.append(clip)
            current_time += highlight.get('duration', 0)

        # Add outro
        outro = structure.get('outro', {})
        if outro.get('duration', 0) > 0:
            clips.append({
                'id': 'outro-0',
                'type': 'text',
                'start_time': current_time,
                'duration': outro.get('duration', 3.0),
                'content': outro.get('content', ''),
            })
            current_time += outro.get('duration', 3.0)

        return {
            'total_duration': current_time,
            'clips': clips,
            'num_clips': len(clips),
            'structure': structure,
        }


# Singleton instance
auto_studio_service = AutoStudioService()
