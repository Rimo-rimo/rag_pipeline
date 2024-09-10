from llama_index.core.postprocessor import SentenceTransformerRerank

class Reranker:
    def __init__(self, model_name, top_n, device):
        self.reranker = SentenceTransformerRerank(model=model_name, top_n=top_n, device=device, keep_retrieval_score=True) 

    def rerank(self, nodes: list, query:str):
        """
        - retrieve결과인 nodes와 유저 query를 기반으로 reranking 진행

        Args:
            nodes (list) : 라마인덱스의 NodeWithScore 객체의 리스트
            query (str) : user의 query
            
        Returns:
            postprocessed nodes (list) : reranking된 NodeWithScore 객체의 리스트
        """
        return self.reranker.postprocess_nodes(nodes, query_str = query)
