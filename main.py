import asyncio
import re
import google.generativeai as genai
import uvicorn
import os
import sys

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



# Get your API key from https://makersuite.google.com/u/0/app/apikey and replace API_KEY with your key

API_KEY = os.environ.get("API_KEY", "AIzaSyAyknKvyIlJ2KzeFvbhtjlV22DMwnxHv_A")

if API_KEY == "":
    print("Please get the api key from https://makersuite.google.com/u/0/app/apikey and set in env")
    sys.exit(1)

genai.configure(api_key=API_KEY)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
}

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sub")
async def submit(request: Request):
    prompt = """Rewrite the following sentence twice - first to fix grammar issues and second to fully rewrite the sentence to be more clear and enthusiastic.
    Original: There going to love opening they're present
    Fixed Grammar: They're going to love opening their present
    Fully Rewritten: They're going to be so excited to open their presents!
    Original: Your going to love NYC
    Fixed Grammar: You're going to love NYC
    Fully Rewritten: You're going to adore New York City.
    Original: {}
    Fixed Grammar:"""

    try:
        data = await request.json()
        data = jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request")

    text = data["textinput"]
    response = genai.generate_text(**defaults, prompt=prompt.format(text))
    response_text = re.sub(r'{', '', response.result)
    response_text = re.search(r'^(.*?)Fully Rewritten:(.*)$', response_text, re.DOTALL)
    response_text_correct = response_text.group(1).strip()
    response_text_rewritten = response_text.group(2).strip()

    if data["action"] == "correct":
        return {"textoutput": response_text_correct, "action": "correct"}
    elif data["action"] == "rewrite":
        return {"textoutput": response_text_rewritten, "action": "rewrite"}
    else:
        return {"textoutput": response_text, "action": "rewrite"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
