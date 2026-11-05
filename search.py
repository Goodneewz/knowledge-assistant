import json
import math
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = "gemini-embedding-001"   # same name as before
BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def embed_one(text):
    body = {"model": f"models/{EMBED_MODEL}", "content": {"parts": [{"text": text}]}}
    r = requests.post(f"{BASE}/{EMBED_MODEL}:embedContent", json=body,
                      headers={"x-goog-api-key": API_KEY}, timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]["values"]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))            # 1: same as norm_a, but for b
    return dot/(norm_a * norm_b)              # 2: dot divided by (norm_a times norm_b)


def top_k(question, chunks, k=3):
    q = embed_one(question)
    scores = [(cosine(q, c["embedding"]), c) for c in chunks]
    scores.sort(key=lambda pair: pair[0], reverse=True)                    # 3: sort scores, highest first
    return scores[:k]              # 4: only the first k items


def test():
    assert round(cosine([1, 0], [1, 0]), 3) == 1.0
    assert round(cosine([1, 0], [0, 1]), 3) == 0.0
    assert round(cosine([1, 2], [2, 4]), 3) == 1.0
    print("Cosine tests passed")


test()
chunks = json.loads(Path("chunks_embedded.json").read_text(encoding="utf-8"))
questions = [
    "How long do refunds take?",
    "Can I order a cake for my wedding?",
    "Do you have vegan options?",
    "Do you deliver to Abuja?",
    "What time do you close on Sunday?",
    "Who owns the bakery?",
    "Do you sell wedding dresses?",
]
for question in questions:
    print("\nQ:", question)
    for score, chunk in top_k(question, chunks):
        print(f"  {score:.3f}  {chunk['id']}  {chunk['text'][:60]}")