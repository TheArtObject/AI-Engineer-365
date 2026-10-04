import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="AI Playground")

APP_CONTEXT = {
    "provider": "Ollama Cloud",
    "model": "gpt-oss:20b-cloud",
    "backend": "FastAPI",
    "environment": "development",
}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OLLAMA_API_KEY is not set. Copy .env.example to .env and add your key.",
        )

    # Same OpenAI-compatible client; requests go to Ollama Cloud, not api.openai.com.
    client = OpenAI(
        api_key=api_key,
        base_url="https://ollama.com/v1/",
    )
    application_context = "Application context:\n" + "\n".join(
        f"- {key}: {value}" for key, value in APP_CONTEXT.items()
    )
    completion = client.chat.completions.create(
        model="gpt-oss:20b-cloud",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the assistant inside this AI Playground. "
                    "Answer the user's request directly. "
                    "Do not present yourself as ChatGPT. "
                    "Do not claim you lack access to Ollama Cloud: this request "
                    "already reached you through our FastAPI backend."
                ),
            },
            {"role": "system", "content": application_context},
            {"role": "user", "content": request.message},
        ],
    )
    reply = completion.choices[0].message.content or ""
    return ChatResponse(reply=reply)
