from pydantic import BaseModel, Field
from typing import Optional

class VideoQuestionRequest(BaseModel):
    """Request model for asking questions about YouTube videos"""
    video_url: str = Field(..., description="YouTube video URL")
    question: str = Field(..., description="Question to ask about the video")

class VideoQuestionResponse(BaseModel):
    """Response model for video Q&A"""
    video_url: str = Field(..., description="YouTube video URL")
    question: str = Field(..., description="Question that was asked")
    answer: str = Field(..., description="Answer to the question")
    context: str = Field(..., description="Relevant context/timestamps from the transcript")
    success: bool = Field(..., description="Whether the request was successful")
    error: Optional[str] = Field(default=None, description="Error message if request failed")
