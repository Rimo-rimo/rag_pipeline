#############################
# 의존성 관리
#############################

from app.config import settings
from app.rag_core.index_storage import IndexStorage
from app.rag_core.reranker import Reranker


class InstanceManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InstanceManager, cls).__new__(cls)
            cls._instance.init_resources()
        return cls._instance

    def init_resources(self):
        self.index = None
        self.reranker = None

        self.init_index()
        self.init_reranker()

    def init_index(self):
        try:
            self.index = IndexStorage(
                milvus_uri=settings.milvus_vector_store_uri, 
                collection_name=settings.collection_name, 
                embed_model=settings.embedding_model_default
            )
            print("IndexStorage successfully initialized.")
        except Exception as e:
            print(f"Failed to initialize IndexStorage: {e}")
            raise

    def init_reranker(self):
        try:
            self.reranker = Reranker(
                model_name=settings.rerank_model_default, 
                top_n=settings.rerank_top_k, 
                device=settings.device
            )
            print("Reranker successfully initialized.")
        except Exception as e:
            print(f"Failed to initialize Reranker: {e}")
            raise

    def get_index(self):
        return self.index

    def get_reranker(self):
        return self.reranker