from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from gtts import gTTS

app = FastAPI(title="Voice Lab API", version="1.0.0")

# CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/clone")
async def clone_voice(
    text: str = Form(...),
    sample: UploadFile | None = File(None)
):
    """
    Demo endpoint: Accepts an optional voice sample and required text.
    Generates speech audio for the text using gTTS and returns an MP3 stream.
    Note: This is a placeholder for real voice cloning; it does not use the sample to condition the voice.
    """
    cleaned = text.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Text must not be empty")

    try:
        # Generate TTS using Google Text-to-Speech (gTTS)
        tts = gTTS(cleaned)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        headers = {
            "Content-Disposition": "inline; filename=cloned.mp3"
        }
        return StreamingResponse(buf, media_type="audio/mpeg", headers=headers)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
