import PyPDF2
from fastapi import UploadFile
import io

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000  # 청크 크기 설정
        
    async def process_pdf(self, file: UploadFile) -> list:
        # PDF 파일 읽기
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        
        # PDF 텍스트 추출
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text()
            
        # 텍스트를 청크로 분할
        chunks = self._split_into_chunks(text_content)
        return chunks
    
    def _split_into_chunks(self, text: str) -> list:
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= self.chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks 