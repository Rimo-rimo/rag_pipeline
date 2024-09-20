#######################
# 검색 및 rerank service
#######################

from app.rag_core.instance_manager import get_instance_manager
from app.schemas import RetrievalRequest


class RetrievalService():
    def __init__(self, index, reranker):
        self.index = index
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
        retrieved_nodes = self.index.search(request.query)
        
        # Reranker를 사용하여 검색 결과를 재정렬
        reranked_nodes = self.reranker.rerank(retrieved_nodes, request.query)

        return reranked_nodes
        