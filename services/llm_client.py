import httpx
from typing import Optional, Tuple
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMClient:
    """Client for asking questions about video transcripts"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto"):
        self.client = httpx.AsyncClient(timeout=60.0)
        
        # Get API key from environment if not provided
        if not api_key:
            groq_key = os.getenv("GROQ_API_KEY")
            
            if groq_key:
                self.api_key = groq_key
                self.provider = "groq"
            else:
                self.api_key = None
                self.provider = "groq"  # default to groq
        else:
            self.api_key = api_key
            # Auto-detect provider based on API key format
            if api_key.startswith("gsk_"):
                self.provider = "groq"
            else:
                self.provider = "groq"  # default to groq
        
        # Set base URL based on provider
        if self.provider == "groq":
            self.base_url = "https://api.groq.com/openai/v1"
        else:
            raise ValueError("Provider must be 'groq'")
    
    async def ask_question(self, transcript: str, question: str) -> Tuple[str, str]:
        """Ask a question about the transcript and return answer with context"""
        
        if not self.api_key:
            raise Exception("No API key found. Set GROQ_API_KEY environment variable.")
        
        # Truncate transcript if too long (most APIs have token limits)
        max_tokens = 4000
        if len(transcript) > max_tokens:
            transcript = transcript[:max_tokens] + "..."
        
        prompt = f"""You are a helpful assistant that answers questions about YouTube video transcripts.

TRANSCRIPT:
{transcript}

QUESTION: {question}

Please provide:
1. A clear and accurate answer to the question
2. The relevant context from the transcript (including approximate timestamps if mentioned)

Format your response as:
ANSWER: [your answer here]
CONTEXT: [relevant context with timestamps if available]"""

        try:
            response = await self._call_groq(prompt)
            
            # Parse the response to extract answer and context
            answer, context = self._parse_response(response)
            
            return answer, context
            
        except Exception as e:
            raise Exception(f"Failed to get answer: {str(e)}")
    
    async def _call_groq(self, prompt: str) -> str:
        """Call Groq API"""
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",  # Fast and cost-effective model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            error_msg = f"Groq API request failed with status {response.status_code}: {response.text}"
            raise Exception(error_msg)

    
    
    def _parse_response(self, response: str) -> Tuple[str, str]:
        """Parse the LLM response to extract answer and context"""
        lines = response.split('\n')
        answer = ""
        context = ""
        
        in_answer = False
        in_context = False
        
        for line in lines:
            line = line.strip()
            if line.startswith("ANSWER:"):
                in_answer = True
                in_context = False
                answer = line.replace("ANSWER:", "").strip()
            elif line.startswith("CONTEXT:"):
                in_answer = False
                in_context = True
                context = line.replace("CONTEXT:", "").strip()
            elif in_answer and line:
                answer += " " + line
            elif in_context and line:
                context += " " + line
        
        # If parsing failed, return the whole response as answer
        if not answer and not context:
            return response, "No specific context provided"
        
        return answer.strip(), context.strip()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
