import os, json, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse(text):
    prompt = f"""Extract receipt data. Return ONLY valid JSON, no markdown.
Format: {{"merchant":"","date":"","items":[{{"name":"","price":"","category":""}}],"total":""}}
Prices must be numeric strings only.
OCR Text: {text}"""
    try:
        raw = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
        return json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group(0))
    except Exception as e:
        return {"error": str(e)}