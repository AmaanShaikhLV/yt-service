from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Any
import re

class TranscriptService:
    """Service for handling YouTube transcript operations"""
    
    def __init__(self):
        self.transcript_cache = {}
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a video ID
        return url
    
    async def get_transcript(self, video_id_or_url: str, languages: List[str] = None) -> str:
        """Get transcript for a YouTube video"""
        if not languages:
            languages = ['en', 'en-US', 'en-GB']
        
        # Extract video ID if URL is provided
        video_id = self.extract_video_id(video_id_or_url)
        
        # Check cache first
        if video_id in self.transcript_cache:
            return self.transcript_cache[video_id]
        
        try:
            # Try to get transcript in preferred languages
            transcript_api = YouTubeTranscriptApi()
            transcript_data = transcript_api.fetch(video_id, languages=languages)
            
            # Combine all transcript parts into a single text
            full_transcript = ""
            for transcript_part in transcript_data:
                full_transcript += transcript_part.text + " "
            
            # Clean up the transcript
            full_transcript = self._clean_transcript(full_transcript)
            
            # Cache the result
            self.transcript_cache[video_id] = full_transcript
            
            return full_transcript
            
        except Exception as e:
            raise Exception(f"Failed to get transcript for video {video_id}: {str(e)}")
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean and format the transcript text"""
        # Remove extra whitespace
        transcript = re.sub(r'\s+', ' ', transcript)
        
        # Remove common transcript artifacts
        transcript = re.sub(r'\[.*?\]', '', transcript)  # Remove bracketed text
        transcript = re.sub(r'\(.*?\)', '', transcript)  # Remove parenthetical text
        
        # Clean up punctuation
        transcript = transcript.strip()
        
        return transcript
    
    async def get_transcript_with_timestamps(self, video_id_or_url: str, languages: List[str] = None) -> List[Dict[str, Any]]:
        """Get transcript with timestamps for a YouTube video"""
        if not languages:
            languages = ['en', 'en-US', 'en-GB']
        
        video_id = self.extract_video_id(video_id_or_url)
        
        try:
            transcript_api = YouTubeTranscriptApi()
            transcript_data = transcript_api.fetch(video_id, languages=languages)
            return transcript_data
            
        except Exception as e:
            raise Exception(f"Failed to get transcript with timestamps for video {video_id}: {str(e)}")
    
    def clear_cache(self):
        """Clear the transcript cache"""
        self.transcript_cache.clear()
