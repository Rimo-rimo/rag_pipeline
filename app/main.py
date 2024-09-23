"""
=====================================================================
FastAPI 실행을 위한 최상단 main 코드
=====================================================================
"""
from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI

from app.routers import index_router, retrieval_router
from app.config import settings
from app.instance_manager import get_instance_manager

# .env 파일 로드
load_dotenv()

# FastAPI 애플리케이션 초기화
app = FastAPI()

# 라우터 추가
app.include_router(index_router.router, prefix="/index", tags=["index"])
# app.include_router(retrieval_router.router, prefix="/retrieval", tags=["retrieval"])

# 애플리케이션 시작 시 실행할 코드
@app.on_event("startup")
def startup_event():
    get_instance_manager()
    print("Load Instance Manager")
    

# 기본 라우트
@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG Pipeline API"}

if __name__ == "__main__":
    # Uvicorn을 사용하여 FastAPI 애플리케이션 실행
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)

