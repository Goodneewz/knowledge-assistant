import json
from pathlib import Path

def chunk_text(text, size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        piece = text[start:start + size].strip()
        if piece:
            chunks.append(piece)
        start += size - overlap
    return chunks

all_chunks = []
files = sorted(Path("docs").glob("*.txt"))
for path in files:
    text = path.read_text(encoding="utf-8")
    for i, piece in enumerate(chunk_text(text)):
        all_chunks.append({"id": f"{path.stem}-{i}", "source": path.name, "text": piece})

Path("chunks.json").write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")
print(f"{len(all_chunks)} chunks from {len(files)} files")