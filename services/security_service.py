import os
from dotenv import load_dotenv

load_dotenv()

class SecurityService:
    def __init__(self):
        self.api_key = os.getenv("API_SECRET_KEY")
        
    def verify_api_key(self, provided_key: str) -> bool:
        if not provided_key:
            return False
        return provided_key == self.api_key 