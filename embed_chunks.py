import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = "gemini-embedding-001"   # use the name from your list
BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def embed_many(texts):
    body = {"requests": [
        {"model": f"models/{EMBED_MODEL}", "content": {"parts": [{"text": t}]}}
        for t in texts
    ]}
    r = requests.post(f"{BASE}/{EMBED_MODEL}:batchEmbedContents", json=body,
                      headers={"x-goog-api-key": API_KEY}, timeout=60)
    r.raise_for_status()
    return [e["values"] for e in r.json()["embeddings"]]


chunks = json.loads(Path("chunks_v2.json").read_text(encoding="utf-8"))
vectors = embed_many([c["text"] for c in chunks])
for chunk, vector in zip(chunks, vectors):
    chunk["embedding"] = vector

Path("chunks_embedded.json").write_text(json.dumps(chunks), encoding="utf-8")
print(len(chunks), "chunks embedded; each vector has", len(vectors[0]), "numbers")