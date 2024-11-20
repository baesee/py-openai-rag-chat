from fastapi import Request, HTTPException
from services.security_service import SecurityService

class SecurityMiddleware:
    def __init__(self):
        self.security_service = SecurityService()
        # API 키 검증이 필요없는 엔드포인트 리스트
        self.public_paths = {"/test", "/docs", "/openapi.json", "/redoc"}
    
    async def __call__(self, request: Request, call_next):
        # 공개 경로는 검증 없이 통과
        if request.url.path in self.public_paths:
            return await call_next(request)
            
        # API 키 추출 (blg-wr-api-key 헤더에서)
        api_key = request.headers.get("blg-wr-api-key")
        
        # API 키 검증
        if not self.security_service.verify_api_key(api_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
            
        # 검증 통과 후 다음 미들웨어/엔드포인트로 진행
        return await call_next(request) 