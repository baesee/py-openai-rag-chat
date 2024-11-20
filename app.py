from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv
from services.pdf_service import PDFProcessor
from services.rag_service import RAGService
from services.security_service import SecurityService
from services.chatgpt_service import ChatGPTService

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

# 서비스 인스턴스 생성
pdf_processor = PDFProcessor()
rag_service = RAGService()
security_service = SecurityService()
chatgpt_service = ChatGPTService()

@app.post("/process-pdf")
async def process_pdf(
    file: UploadFile = File(...),
    source: str = Form(...),
    api_key: Optional[str] = Header(None)
):
    # API 키 검증
    if not security_service.verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # PDF 처리 및 벡터화 (출처 정보 포함)
        text_chunks = await pdf_processor.process_pdf(file, source)
        vector_ids = await rag_service.vectorize_and_store(text_chunks)
        
        return {"status": "success", "message": "PDF processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(
    question: str,
    api_key: Optional[str] = Header(None)
):
    # API 키 검증
    if not security_service.verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # RAG 기반 답변 생성
        answer = await rag_service.generate_answer(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.post("/chat")
async def chat(
    prompt: str,
    api_key: Optional[str] = Header(None)
):
    # API 키 검증
    if not security_service.verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # ChatGPT 응답 생성
        response = await chatgpt_service.generate_response(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hello")
async def hello(
    api_key: Optional[str] = Header(None)
):
    if not security_service.verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {"message": "hello python"}

@app.get("/test")
async def test():
    return {"message": "hello test"}