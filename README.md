# YouTube Video Q&A Service

A simple FastAPI service that lets you ask questions about YouTube videos. The system extracts the video transcript and uses AI to answer your questions with relevant context.

## Features

- 🎥 Extract transcripts from YouTube videos
- 🤖 Ask questions about video content using AI
- 📍 Get answers with relevant context and timestamps
- 🌐 Simple, clean web interface
- 🔄 Support for both OpenAI and OpenRouter APIs

## How It Works

1. **Input**: User provides a YouTube video URL and asks a question
2. **Transcript**: System extracts the video transcript
3. **AI Analysis**: Sends transcript + question to language model
4. **Response**: Returns answer with relevant context from the video

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key OR OpenRouter API key

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key**
   ```bash
   # For OpenAI
   export OPENAI_API_KEY="your-openai-api-key"
   
   # OR for OpenRouter
   export OPENROUTER_API_KEY="your-openrouter-api-key"
   ```

3. **Run the service**
   ```bash
   python main.py
   ```

4. **Open in browser**
   - Go to `http://localhost:8000`
   - Enter a YouTube URL and ask a question!

## API Usage

### POST `/ask`

Ask a question about a YouTube video.

**Request:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "question": "What is the main topic of this video?"
}
```

**Response:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "question": "What is the main topic of this video?",
  "answer": "The main topic is...",
  "context": "Relevant context from the video with timestamps...",
  "success": true
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### LLM Provider

The service supports both OpenAI and OpenRouter. Set the appropriate API key:

- **OpenAI**: Set `OPENAI_API_KEY` environment variable
- **OpenRouter**: Set `OPENROUTER_API_KEY` environment variable

## Example Questions

- "What is the main topic of this video?"
- "What are the key points discussed?"
- "What does the speaker say about [specific topic]?"
- "What are the conclusions reached?"
- "What examples are given?"

## Project Structure

```
├── main.py                 # FastAPI application
├── services/
│   ├── transcript.py       # YouTube transcript extraction
│   └── llm_client.py       # AI Q&A client
├── models/
│   └── schemas.py          # API request/response models
├── frontend/
│   └── index.html          # Web interface
└── requirements.txt        # Python dependencies
```

## Troubleshooting

### Common Issues

1. **"API key not provided"**
   - Make sure you've set the correct environment variable
   - Check that the API key is valid

2. **"Failed to get transcript"**
   - Video might not have captions/transcript
   - Check if the YouTube URL is valid
   - Some videos may be private or restricted

3. **"Network error"**
   - Check your internet connection
   - Verify the API service is accessible

### Tips

- Use videos with good quality captions for better results
- Be specific with your questions
- The system works best with English content

## License

This project is open source and available under the MIT License.
