import dotenv
import os
import logging
dotenv.load_dotenv()

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embed_model: str, collection_name:str):
        self.collection_name = collection_name
        self.embed_model, self.embed_dim = self._select_embed_model(embed_model)
        self.vector_store = self._init_vector_store(collection_name)
        self.index = self._init_index()

    def _select_embed_model(embed_model):
        """
        - 임베딩 모델 선택 및 벡터 차원 설정.

        Args:
            embed_model (str): 사용할 모델 타입 ('bge-m3' 또는 'openai')

        Returns:
            tuple: 선택한 임베딩 모델 인스턴스와 벡터 차원 값
        """
        if embed_model == 'bge-m3':
            logger.info("Using HuggingFace BGE-M3 model.")
            model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
            dim = 1024  # HuggingFace 모델의 벡터 차원
        elif embed_model == 'openai':
            logger.info("Using OpenAI Embedding model.")
            model = OpenAIEmbedding(model="text-embedding-3-large")
            dim = 1536  # OpenAI 모델의 벡터 차원
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return model, dim
    
    def _init_vector_store(self, collection_name):
        """
        Milvus 벡터 스토어 초기화

        Args:
            collection_name (str): 벡터 스토어의 컬렉션 이름

        Returns:
            MilvusVectorStore: 초기화된 Milvus 벡터 스토어 인스턴스
        """
        try:
            vector_store = MilvusVectorStore(
                uri=os.getenv("MILVUS_VECTOR_STORE_URI"),
                collection_name=collection_name,
                overwrite=False,
                dim=self.dim  # 임베딩 모델에 따라 설정된 dim 사용
            )
            logger.info(f"Milvus Vector Store initialized with collection: {collection_name}")
            return vector_store
        except Exception as e:
            logger.error(f"Failed to initialize Milvus Vector Store: {e}")
            raise
    
    def _init_index(self):
        index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store,
            embed_model = self.embed_model,
            show_progress=True)
        return index
    
    def insert(self, nodes):
        try:
            self.index.insert_nodes(nodes, show_progress=True)
            logger.info(f"Insert {len(nodes)} nodes.")
        except Exception as e:
            logger.error(f"Failed to insert nodes in Milvus Vector Store: {e}")
            raise

    def delete(self):
        pass

    def refresh(self):
        pass