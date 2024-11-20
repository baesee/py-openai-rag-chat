import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT

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
        
        # 시스템 프롬프트 설정
        self.system_template = """
        당신은 주어진 문서를 기반으로 답변하는 전문가입니다.
        다음 원칙을 반드시 따라주세요:
        1. 주어진 문서의 내용만을 기반으로 답변하세요.
        2. 답변에 출처를 꼭 남겨주세요
        3. 문서에 없는 내용은 "문서에서 해당 내용을 찾을 수 없습니다"라고 답변하세요.
        4. 답변은 항상 친절하고 전문적으로 제공하세요.
        5. 필요한 경우 문서의 관련 내용을 인용하여 설명하세요.

        Context: {context}
        Question: {question}
        """
        
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
            
        # 사용자 정의 프롬프트 템플릿 생성
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ])
        
        # 검색 체인 생성 (사용자 정의 프롬프트 적용)
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.chat_model,
            retriever=self.vector_store.as_retriever(),
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        # 질문에 대한 답변 생성
        result = qa_chain({"question": question, "chat_history": []})
        return result["answer"]
        
    # 시스템 프롬프트 동적 업데이트를 위한 메서드
    def update_system_template(self, new_template: str):
        self.system_template = new_template