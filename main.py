from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import mammoth
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract")
async def extract_docx(file: UploadFile, client_id: str = Form(...)):
    content = await file.read()
    result = mammoth.convert_to_html(content)
    html = result.value
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return {
        "client_id": client_id,
        "text": text
    }
