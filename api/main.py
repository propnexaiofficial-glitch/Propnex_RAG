import os, io, tempfile, subprocess
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import librosa
import soundfile as sf

os.environ["COQUI_TOS_AGREED"] = "1"
REF_WAV = os.getenv("REF_WAV", "assets/reference.wav")
API_KEY = os.getenv("SERVER_API_KEY", "")
models = {}


@asynccontextmanager
async def lifespan(app):
    from faster_whisper import WhisperModel
    from TTS.api import TTS
    from src.pipeline import answer
    models["stt"] = WhisperModel("large-v3", device="cuda", compute_type="float16")
    models["tts"] = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
    models["answer"] = answer
    yield


app = FastAPI(lifespan=lifespan)


def check(key):
    if not API_KEY or key != API_KEY:
        raise HTTPException(status_code=401, detail="bad key")


class Q(BaseModel):
    question: str


class T(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/stt")
async def stt(file: UploadFile = File(...), x_api_key: str | None = Header(None)):
    check(x_api_key)
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        f.write(await file.read())
        src = f.name
    dst = src + ".wav"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", dst],
            check=True, capture_output=True,
        )
        audio, _ = librosa.load(dst, sr=16000, mono=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="audio decode failed")
    finally:
        for p in (src, dst):
            if os.path.exists(p):
                os.remove(p)
    segs, _ = models["stt"].transcribe(
        audio, language="hi", beam_size=1,
        initial_prompt="प्रॉपनेक्स एआई टेक्नोलॉजी, तनिष्क गुप्ता, वॉइस एजेंट",
    )
    return {"text": " ".join(s.text for s in segs).strip()}


@app.post("/answer")
def answer_ep(q: Q, x_api_key: str | None = Header(None)):
    check(x_api_key)
    r = models["answer"](q.question)
    return {"answer": r["answer"], "search_query": r["search_query"]}


@app.post("/tts")
def tts_ep(t: T, x_api_key: str | None = Header(None)):
    check(x_api_key)
    wav = models["tts"].tts(text=t.text, speaker_wav=REF_WAV, language="hi")
    buf = io.BytesIO()
    sf.write(buf, wav, 24000, format="WAV")
    return Response(content=buf.getvalue(), media_type="audio/wav")