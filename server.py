from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app import chat  # your existing logic

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    session_id: str = None  # optional

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    def stream_with_context(query):
        for chunk in chat(query):
            yield chunk

    return StreamingResponse(stream_with_context(req.query), media_type="text/event-stream")



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render sets this dynamically
    uvicorn.run("server:app", host="0.0.0.0", port=80, reload=True)


