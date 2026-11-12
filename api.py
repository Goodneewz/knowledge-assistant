from fastapi import FastAPI
from rag import answer

app = FastAPI()


@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/ask")
def ask(question: str):
    return {"question": question, "answer": answer(question)}