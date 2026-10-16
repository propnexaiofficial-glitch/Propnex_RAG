import os, io, time, tempfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import librosa
import soundfile as sf

os.environ["COQUI_TOS_AGREED"] = "1"
REF_WAV = os.getenv("REF_WAV", "assets/reference.wav")
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


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/voice")
async def voice(file: UploadFile = File(...)):
    t0 = time.time()
    with tempfile.NamedTemporaryFile(suffix=".audio", delete=False) as f:
        f.write(await file.read())
        path = f.name
    audio, _ = librosa.load(path, sr=16000, mono=True)
    os.remove(path)

    segs, _ = models["stt"].transcribe(
        audio, language="hi", beam_size=1,
        initial_prompt="प्रॉपनेक्स एआई टेक्नोलॉजी, तनिष्क गुप्ता, वॉइस एजेंट",
    )
    question = " ".join(s.text for s in segs).strip()
    t1 = time.time()

    reply = models["answer"](question)["answer"]
    t2 = time.time()

    wav = models["tts"].tts(text=reply, speaker_wav=REF_WAV, language="hi")
    buf = io.BytesIO()
    sf.write(buf, wav, 24000, format="WAV")
    t3 = time.time()

    return Response(
        content=buf.getvalue(),
        media_type="audio/wav",
        headers={
            "X-Question": question.encode("unicode_escape").decode(),
            "X-Timing": f"stt={t1-t0:.1f},rag={t2-t1:.1f},tts={t3-t2:.1f}",
        },
    )