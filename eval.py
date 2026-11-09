import json
from pathlib import Path
from rag import answer
import time

REFUSAL = "I don't have that information"

tests = json.loads(Path("tests.json").read_text(encoding="utf-8"))
counts = {"correct_answer": 0, "false_refusal": 0, "wrong_answer": 0,
          "correct_refusal": 0, "false_answer": 0}

for t in tests:
    reply = answer(t["q"])
    refused = REFUSAL in reply
    if t["should_refuse"]:
        key = "correct_refusal" if refused else "false_answer"      # blank 1: "correct_refusal" if refused, else "false_answer"
    else:
        if refused:
            key = "false_refusal"
        elif t["expect"].lower() in reply.lower():
            key = "correct_answer"
        else:
            key = "wrong_answer"            # blank 2: set key with if / elif / else (see below)
    counts[key] += 1
    print(key, "|", t["q"])
    time.sleep(4)

print(counts)