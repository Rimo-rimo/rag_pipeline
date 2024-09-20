#############################
# 의존성 관리
#############################

from app.config import settings
from app.rag_core.index_storage import IndexStorage
from app.rag_core.reranker import Reranker
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding


class InstanceManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InstanceManager, cls).__new__(cls)
            cls._instance.init_resources()
        return cls._instance

    def init_resources(self):
        self.embed_model = None
        self.embed_dim = None
        # self.index = None
        self.reranker = None

        self.init_embed_model()
        self.init_reranker()

    # def init_index(self):
    #     try:
    #         self.index = IndexStorage(
    #             milvus_uri=settings.milvus_vector_store_uri, 
    #             collection_name=settings.collection_name, 
    #             embed_model=settings.embedding_model_default
    #         )
    #         print("IndexStorage successfully initialized.")
    #     except Exception as e:
    #         print(f"Failed to initialize IndexStorage: {e}")
    #         raise

    def init_embed_model(self, embed_model=settings.embedding_model_default):
        if embed_model == 'bge-m3':
            self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
            self.embed_dim = 1024  # HuggingFace 모델의 벡터 차원
            print("HuggingFace BGE-M3 model successfully initialized.")
        elif embed_model == 'openai':
            self.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
            self.embed_dim = 1536  # OpenAI 모델의 벡터 차원
            print("OpenAI Embedding model successfully initialized.")
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

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
    
    def get_embed_model(self):
        return self.embed_model
    
    # def get_index(self):
    #     return self.index

    def get_reranker(self):
        return self.reranker

def get_instance_manager():
    return InstanceManager()
