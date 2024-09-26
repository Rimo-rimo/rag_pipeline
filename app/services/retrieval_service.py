#######################
# 검색 및 rerank service
#######################

from app.rag_core.index_storage import get_index
from app.schemas import RetrievalRequest, ChatRequest


class RetrievalService():
    def __init__(self, embed_model, reranker, embed_dim: int, collection_name: str, milvus_uri: str):
        self.index = get_index(embed_model = embed_model,
                        embed_dim = embed_dim,
                        collection_name = collection_name,
                        milvus_uri = milvus_uri)

        self.reranker = reranker
    
    def retrieve(self, request: RetrievalRequest):
        """
        - user query를 기반으로 index에서 retrieval 진행

        Args:
            request (RetrievalRequest) : user query

        Returns:
            retrieved nodes (list) : retrieval된 NodeWithScore 객체의 리스트
        """
        # Index에서 검색 수행
        retrieved_nodes = self.index.retrieve(query=request.query, similarity_top_k=request.top_n)

        # Reranker를 사용하여 검색 결과를 재정렬
        # if request.is_rerank:
        #     retrieved_nodes = self.reranker.rerank(retrieved_nodes, request.query)

        return retrieved_nodes

        