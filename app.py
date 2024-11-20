from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv
from services.pdf_service import PDFProcessor
from services.rag_service import RAGService
from services.chatgpt_service import ChatGPTService
from middleware.security_middleware import SecurityMiddleware
import urllib.parse

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 보안 미들웨어 추가
app.middleware("http")(SecurityMiddleware())

# 서비스 인스턴스 생성
pdf_processor = PDFProcessor()
rag_service = RAGService()
chatgpt_service = ChatGPTService()

@app.post("/process-pdf")
async def process_pdf(
    file: UploadFile = File(...),
    source: str = Form(...)
):
    try:
        text_chunks = await pdf_processor.process_pdf(file, source)
        vector_ids = await rag_service.vectorize_and_store(text_chunks)
        return {"status": "success", "message": "PDF processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(question: str):
    try:
        decoded_question = urllib.parse.unquote(question)
        answer = await rag_service.generate_answer(decoded_question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(prompt: str):
    try:
        response = await chatgpt_service.generate_response(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hello")
async def hello():
    return {"message": "hello python"}

@app.get("/test")
async def test():
    return {"message": "hello test"}