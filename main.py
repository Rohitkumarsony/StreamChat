import socketio
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.router.chat_router import sio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# Initialize FastAPI app
app= FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
uploads_dir = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# Mount the static directory
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "title": "Chat Room"
    })


# Mount the Socket.IO app AFTER defining all routes
app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")