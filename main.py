from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from services.transcript import TranscriptService
from services.llm_client import LLMClient
from models.schemas import VideoQuestionRequest, VideoQuestionResponse

app = FastAPI(title="YouTube Q&A Service", description="Ask questions about YouTube videos")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize services
transcript_service = TranscriptService()
llm_client = LLMClient()

@app.get("/")
async def root():
    """Serve the frontend HTML file"""
    return FileResponse("frontend/index.html")

@app.post("/ask", response_model=VideoQuestionResponse)
async def ask_question(request: VideoQuestionRequest):
    """Ask a question about a YouTube video"""
    try:
        # Get the transcript
        transcript = await transcript_service.get_transcript(request.video_url)
        
        # Ask the question using LLM
        answer, context = await llm_client.ask_question(transcript, request.question)
        
        return VideoQuestionResponse(
            video_url=request.video_url,
            question=request.question,
            answer=answer,
            context=context,
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "youtube-qa-service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
