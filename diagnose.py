import json
from pathlib import Path
from search import top_k

chunks = json.loads(Path("chunks_embedded.json").read_text(encoding="utf-8"))
tests = json.loads(Path("tests.json").read_text(encoding="utf-8"))

failing = [
    "Do you only make cakes?",
    "Do I have to pay extra to change the design?",
    "Where is your shop located?",
]

for t in tests:
    if t["q"] not in failing:
        continue
    hits = top_k(t["q"], chunks, k=3)
    found = any(t["expect"].lower() in c["text"].lower() for score, c in hits)
    print("\nQ:", t["q"])
    print("Expected word:", t["expect"], "| in top 3 chunks?", found)
    for score, c in hits:
        print(f"  {score:.3f} {c['id']}")