import json
from pathlib import Path
from chat import ask_with_retry
from search import top_k

SYSTEM = """You are the customer assistant for Mama Tee's Bakery.
Rules:
1. Use ONLY the facts in the CONTEXT. Never use outside knowledge.
2. You may draw simple, logical conclusions from those facts.
   Example 1: if the CONTEXT says "We deliver within Lagos only", then for
   "Do you deliver to Abuja?" answer: "No, we deliver within Lagos only. [04_delivery-0]"
    Example 2: if the CONTEXT lists "pizza, pasta and salad", then for
   "Do you only sell pizza?" answer: "No, we also sell pasta and salad. [menu-0]"
3. After each fact, cite the chunk id in square brackets, like [04_delivery-0].
4. Only if the CONTEXT has nothing relevant to the question, reply exactly:
I don't have that information. Please message us on WhatsApp: +234 800 000 0000.
5. Never guess."""

chunks = json.loads(Path("chunks_embedded.json").read_text(encoding="utf-8"))


def answer(question):
    hits = top_k(question, chunks, k=15)
    context = "\n".join(f"[{c['id']}] {c['text']}" for score, c in hits)
    messages = [{"role": "user", "parts": [{"text": f"CONTEXT:\n{context}\n\nQUESTION: {question}"}]}]
    text, usage = ask_with_retry(messages, system=SYSTEM, temperature=0)
    return text


if __name__ == "__main__":
    questions = [
        "How long do refunds take?",
        "Can I order a cake for my wedding?",
        "Do you have vegan options?",
        "Do you deliver to Abuja?",
        "What time do you close on Sunday?",
        "Who owns the bakery?",
        "Do you sell wedding dresses?",
    ]
    for q in questions:
        print(q)    # print the question
        print(answer(q))    # print the answer by calling answer(q)
        print()