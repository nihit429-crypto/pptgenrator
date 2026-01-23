import os
from io import BytesIO
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv
from .schemas import GenerateRequest
from .groq_llm import generate_outline
from .pptx_builder import build_pptx

load_dotenv()
app = FastAPI(title="PPTX Generator")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Cache both outline AND built pptx (thread-safe)
import logging
import time
from threading import Lock

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_cache = {}
_cache_lock = Lock()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/preview")
def preview(topic: str = Form(...), num_slides: int = Form(...)):
    try:
        req = GenerateRequest(topic=topic, num_slides=num_slides)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        # Generate content
        outline = generate_outline(req.topic, req.num_slides)
        
        # Build PPTX NOW (so download is instant)
        pptx_bytes = build_pptx(outline)
        # Create a unique download key so multiple users don't clobber each other
        key = f"{req.topic}:{req.num_slides}:{int(time.time()*1000)}"
        with _cache_lock:
            _cache[key] = pptx_bytes
        
        return JSONResponse({
            "title": outline.presentation_title,
            "subtitle": outline.subtitle,
            "download_key": key,
            "slides": [
                {
                    "title": s.title,
                    "bullets": s.bullets,
                    "image": f"https://source.unsplash.com/400x300/?{s.image_keyword}" if s.image_keyword else ""
                }
                for s in outline.slides
            ]
        })
    except Exception as e:
        logger.exception("Generation failed")
        raise HTTPException(status_code=500, detail="Generation failed, try again later")

@app.post("/download")
def download(key: str = Form(...)):
    with _cache_lock:
        pptx = _cache.pop(key, None)
    if not pptx:
        raise HTTPException(status_code=400, detail="Presentation not found or expired")
    
    # Instant download - already built!
    return StreamingResponse(
        BytesIO(pptx),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=presentation.pptx"}
    )