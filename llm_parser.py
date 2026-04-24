import os, json, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse(text):
    prompt = f"""
You are an expert receipt parser.

STRICT RULES:
- Extract only clearly readable items
- Do NOT guess missing values
- Ignore unclear or broken lines
- Prices must be realistic numbers (no random large values)
- If no valid items → return empty list

Return ONLY valid JSON (no markdown):

{{
  "items":[{{"name":"","price":"","category":""}}],
  "total":""
}}

OCR TEXT:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content.strip()

        # remove ```json blocks
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)

        # extract JSON safely
        match = re.search(r"\{.*\}", raw, re.DOTALL)

        if match:
            return json.loads(match.group(0))
        else:
            return {"items": [], "total": ""}

    except Exception as e:
        return {"error": str(e)}
