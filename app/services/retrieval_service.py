#######################
# 검색 및 rerank service
#######################

from app.db import get_index
from app.schemas import RetrievalRequest
from app.rag_core.index_storage import IndexStorage
from app.rag_core.reranker import Reranker


class RetrievalService():
    def __init__(self, index: IndexStorage, ):
        pass
    