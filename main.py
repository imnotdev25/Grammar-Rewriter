from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import re
import uvicorn

# Get your API key from https://makersuite.google.com/u/0/app/apikey and replace API_KEY with your key
genai.configure(api_key="API_KEY")
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


@app.post("/submit")
async def submit(request: Request, text: str = Form(...)):

    prompt = """Rewrite the following sentence twice - first to fix grammar issues and second to fully rewrite the sentence to be more clear and enthusiastic.
    Original: There going to love opening they're present
    Fixed Grammar: They're going to love opening their present
    Fully Rewritten: They're going to be so excited to open their presents!
    Original: Your going to love NYC
    Fixed Grammar: You're going to love NYC
    Fully Rewritten: You're going to adore New York City.
    Original: {}
    Fixed Grammar:"""
    response = genai.generate_text(**defaults, prompt=prompt.format(text))
    response_text = re.sub(r'{', '', response.result)
    return templates.TemplateResponse("index.html", {"request": request, "response_text": response_text, "text": text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
