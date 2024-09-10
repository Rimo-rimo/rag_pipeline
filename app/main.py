"""
=====================================================================
FastAPI 실행을 위한 최상단 main 코드
=====================================================================
"""
from dotenv import load_dotenv
import os

import uvicorn
from fastapi import FastAPI

from core.directory_event_handler import Handler
from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from core.reranker import Reranker

# .env 파일 로드
load_dotenv()

