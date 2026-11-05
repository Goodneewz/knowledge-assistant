import json
import re
from pathlib import Path


def chunk_by_sentences(text, max_chars=400):
    text = " ".join(text.split())
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        if current == "":
            current = sentence
        elif len(current) + 1 + len(sentence) <= max_chars:
            current += " " + sentence      # 1: add a space, then the sentence, to current
        else:
            chunks.append(current)                # 2: save current into the chunks list
            current = sentence      # 3: start a new current with this sentence
    if current != "":
        chunks.append(current)                    # 4: save the last current into the chunks list
    return chunks


def test():
    assert chunk_by_sentences("Aaa. Bbb. Ccc. Ddd.", 10) == ["Aaa. Bbb.", "Ccc. Ddd."]
    assert chunk_by_sentences("Aaa. Bbb. Ccc. Ddd.", 5) == ["Aaa.", "Bbb.", "Ccc.", "Ddd."]
    assert chunk_by_sentences("One very long sentence here.", 5) == ["One very long sentence here."]
    print("All tests passed")


test()

all_chunks = []
for path in sorted(Path("docs").glob("*.txt")):
    text = path.read_text(encoding="utf-8")
    for i, piece in enumerate(chunk_by_sentences(text, 400)):
        all_chunks.append({"id": f"{path.stem}-{i}", "source": path.name, "text": piece})

Path("chunks_v2.json").write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")
print(len(all_chunks), "chunks saved to chunks_v2.json")