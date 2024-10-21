#############################
# 의존성 관리
#############################

from app.config import settings
from app.rag_core.index_storage import IndexStorage
from app.rag_core.reranker import Reranker
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


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
        self.reranker = None
        self.llm = None

        self.init_embed_model()
        self.init_reranker()
        self.init_llm()

    def init_embed_model(self, embed_model=settings.embedding_model_default):
        self.bgem3_embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        self.bgem3_embed_dim = 1024  # HuggingFace 모델의 벡터 차원

        self.openai_embed_model = OpenAIEmbedding(model="text-embedding-3-large")
        self.openai_embed_dim = 3072  # OpenAI 모델의 벡터 차원

    def init_reranker(self):
        try:
            self.reranker = Reranker(
                model_name=settings.rerank_model_default, 
                top_n=settings.rerank_top_k, 
                device=settings.device
            )
            print(f"{settings.rerank_model_default}-Reranker successfully initialized.")
        except Exception as e:
            print(f"Failed to initialize Reranker: {e}")
            raise
    
    def init_llm(self):
        # self.llm = OpenAI(model="gpt-4o")
        self.llm = OpenAI(model="gpt-4o-mini")
    
    def get_embed_model(self):
        return self.embed_model

    def get_reranker(self):
        return self.reranker
    
    def get_llm(self):
        return self.llm

def get_instance_manager():
    return InstanceManager()
