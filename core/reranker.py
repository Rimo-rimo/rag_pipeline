from llama_index.core.postprocessor import SentenceTransformerRerank

class VectorStore:
    def __init__(self, embed_model: str, collection_name:str):
        self.collection_name = collection_name
        self.embed_model, self.embed_dim = self._select_embed_model(embed_model)
        self.vector_store = self._init_vector_store(collection_name)
        self.index = self._init_index()

    # def _select_embed_model(self, embed_model):

class Reranker:
    def __init__(self, model_name, top_n, device):
        self.reranker = SentenceTransformerRerank(model=model_name, top_n=top_n, device=device, keep_retrieval_score=True) 

reranker.postprocess_nodes(result_nodes, query_str = query)