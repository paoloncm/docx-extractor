from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
async def extract_docx(file: UploadFile = File(...), client_id: str = Form(...)):
    try:
        contents = await file.read()

        print(f"📂 Archivo recibido: {file.filename}")
        print(f"📦 Tamaño: {len(contents)} bytes")

        result = mammoth.convert_to_html(contents)
        html = result.value
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")

        return {
            "client_id": client_id,
            "text": text
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
