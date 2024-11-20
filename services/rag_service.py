import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

class RAGService:
    def __init__(self):
        # OpenAI의 임베딩 모델을 초기화하여 텍스트를 벡터로 변환
        self.embeddings = OpenAIEmbeddings()
        
        # 벡터 저장소 초기화 (vectorize_and_store 메서드에서 설정됨)
        self.vector_store = None
        
        # ChatGPT 모델 초기화
        # model_name: 사용할 GPT 모델 지정
        # temperature: 0.7로 설정하여 적당한 창의성 부여
        self.chat_model = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
        
    async def vectorize_and_store(self, text_chunks: list):
        # 텍스트 청크를 벡터화하고 FAISS에 저장
        self.vector_store = FAISS.from_texts(
            text_chunks,
            self.embeddings
        )
        return True
        
    async def generate_answer(self, question: str) -> str:
        if not self.vector_store:
            raise Exception("Vector store is not initialized")
            
        # 검색 체인 생성
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.chat_model,
            retriever=self.vector_store.as_retriever(),
            return_source_documents=True
        )
        
        # 질문에 대한 답변 생성
        result = qa_chain({"question": question, "chat_history": []})
        return result["answer"] 