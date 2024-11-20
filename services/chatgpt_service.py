from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class ChatGPTService:
    def __init__(self):
        self.chat_model = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
    
    async def generate_response(self, prompt: str) -> str:
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}") 