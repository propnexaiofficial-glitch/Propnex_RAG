#!/bin/bash
set -e

cd /workspace/Propnex_RAG

pip install -q faster-whisper coqui-tts hf_transfer
pip install -q fastapi uvicorn python-multipart librosa soundfile
pip install -q chromadb google-genai python-dotenv pypdf python-docx
pip install -q "transformers==4.57.6" "tokenizers==0.22.2" "sentence-transformers==5.7.0"

pkill -f uvicorn || true
nohup uvicorn api.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
echo "Server starting. Check: tail -n 5 server.log"
