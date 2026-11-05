import os
import requests
from dotenv import load_dotenv

load_dotenv()
r = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": os.getenv("GEMINI_API_KEY")},
    timeout=60,
)
r.raise_for_status()
for m in r.json()["models"]:
    if "embedContent" in m.get("supportedGenerationMethods", []):
        print(m["name"])
    #if "generateContent" in m.get("supportedGenerationMethods", []):
    #    print(m["name"])
    
    