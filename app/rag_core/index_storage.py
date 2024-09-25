import dotenv

import os
import logging
dotenv.load_dotenv()

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from pymilvus import Collection, connections
from urllib.parse import urlparse
from app.config import settings

logger = logging.getLogger(__name__)

class IndexStorage:

    def __init__(self, embed_model, embed_dim: int, collection_name: str, milvus_uri: str):
        self.embed_model = embed_model
        self.embed_dim = embed_dim
        self.vector_store = self._init_vector_store(milvus_uri, collection_name)
        self.collection = self._init_collection(milvus_uri, collection_name)
        self.index = self._init_index()
    
    def _init_vector_store(self, milvus_uri, collection_name):
        """
        Milvus 벡터 스토어 초기화

        Args:
            collection_name (str): 벡터 스토어의 컬렉션 이름

        Returns:
            MilvusVectorStore: 초기화된 Milvus 벡터 스토어 인스턴스
        """
        try:
            vector_store = MilvusVectorStore(
                uri=milvus_uri,
                collection_name=collection_name,
                overwrite=False,
                dim=self.embed_dim  # 임베딩 모델에 따라 설정된 dim 사용
            )
            logger.info(f"Milvus Vector Store initialized with collection: {collection_name}")
            return vector_store
        except Exception as e:
            logger.error(f"Failed to initialize Milvus Vector Store: {e}")
            raise

    def _init_collection(self, milvus_uri, collection_name):
        """
        Milvus VectorStore의 collection 추출 

        Args:

        Returns:
            num_entities (int) : entities(nodes)의 개수
        """
        parsed_url = urlparse(milvus_uri)
        hostname = parsed_url.hostname 
        port = parsed_url.port   
        connections.connect("default", host=hostname, port=port)
        return Collection(name=collection_name)
    
    def _init_index(self):
        """
        Index 초기화 함수

        Args:

        Returns:
            라마 인덱스의 VectorStoreIndex 객체
        """
        index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store,
            embed_model = self.embed_model,
            show_progress=True)
        return index
    
    def insert(self, nodes):
        """
        Index에 새로운 nodes 추가

        Args:
            nodes (list): node 객체의 list

        Returns:
        """
        try:
            self.index.insert_nodes(nodes, show_progress=True)
            print(f"Insert {len(nodes)} nodes.")
            self.collection.flush()
            print("Done : collection flush")
            return nodes
        except Exception as e:
            logger.error(f"Failed to insert nodes in Milvus Vector Store: {e}")
            raise

    def delete(self):
        pass

    def refresh(self):
        pass

    def num_entities(self):
        """
        VectorStore에 저장된 entities(nodes)의 개수 추출

        Args:

        Returns:
            num_entities (int) : entities(nodes)의 개수
        """
        return self.collection.num_entities

    def retrieve(self, query: str, similarity_top_k: int = settings.vector_search_top_k):
        """
        Vector Search 진행

        Args:
            query (str) : 쿼리 문장
            similarity_top_k (int) : 검색될 최대 node 개수

        Returns:
            num_entities (int) : entities(nodes)의 개수
        """
        retriever = self.index.as_retriever(similarity_top_k=similarity_top_k)
        return retriever.retrieve(query)

def get_index(embed_model, embed_dim, collection_name: str = settings.collection_name, milvus_uri: str = settings.milvus_vector_store_uri):
    """
    IndexStorage 객체 반환

    Args:

    Returns:
        IndexStorage : IndexStorage 객체
    """
    return IndexStorage(
        embed_model=embed_model,
        embed_dim=embed_dim,
        collection_name=collection_name,
        milvus_uri=milvus_uri
    )