from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app import chat  # your existing logic

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, there!"})

chat_histories = {}

class ChatRequest(BaseModel):
    query: str
    session_id: str  # optional


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    
    if req.session_id not in chat_histories:
        chat_histories[req.session_id] = []
    
    def stream_with_context(query):
        for chunk in chat(query, chat_histories[req.session_id]):
            yield chunk

    return StreamingResponse(stream_with_context(req.query), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)
