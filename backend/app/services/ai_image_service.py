"""AI Image Generation Service - Stable Diffusion integration"""

from typing import Optional, List
import json


class AIImageService:
    """AI image generation using Stable Diffusion or similar"""

    def __init__(self):
        self.provider = "stable-diffusion"
        self.model = "sd-3-medium"

    async def generate_image(
        self,
        prompt: str,
        style: str = "realistic",
        aspect_ratio: str = "16:9",
    ) -> dict:
        """Generate image from text prompt"""

        # In development, return mock data
        return {
            "id": "img-uuid",
            "prompt": prompt,
            "style": style,
            "aspect_ratio": aspect_ratio,
            "image_url": f"s3://bucket/images/img-uuid.png",
            "status": "completed",
            "provider": self.provider,
        }

    async def generate_multiple(
        self,
        prompts: List[str],
        style: str = "realistic",
    ) -> List[dict]:
        """Generate multiple images"""

        images = []
        for i, prompt in enumerate(prompts):
            img = await self.generate_image(prompt, style)
            images.append(img)

        return images

    def suggest_images_for_transcript(
        self,
        transcript_segments: List[dict],
    ) -> List[dict]:
        """Suggest images for transcript segments"""

        suggestions = []

        medical_keywords = [
            'bệnh', 'sức khỏe', 'thuốc', 'điều trị',
            'xét nghiệm', 'phòng ngừa', 'triệu chứng',
            'viêm', 'nhiễm', 'ổn định'
        ]

        for seg in transcript_segments:
            text = seg.get('text', '').lower()

            # Find relevant keywords
            relevant = [kw for kw in medical_keywords if kw in text]

            if relevant:
                prompt = f"Y tế, sức khỏe: {', '.join(relevant[:3])}"
                suggestions.append({
                    'segment_time': seg.get('start_time', 0),
                    'prompt': prompt,
                    'confidence': 0.85,
                })

        return suggestions


# Singleton
ai_image_service = AIImageService()
