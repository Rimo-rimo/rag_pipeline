#######################
# Query & Response
#######################

from app.rag_core.index_storage import get_index
from app.schemas import RetrievalRequest, ChatRequest
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


class ChatService():
    def __init__(self, embed_model, reranker, llm, embed_dim, collection_name: str):
        self.index = get_index(embed_model = embed_model,
                        embed_dim = embed_dim,
                        collection_name = collection_name)

        self.reranker = reranker
        self.llm = llm
    
    def query(self, query: str, top_k: int = 10):
        retriever = VectorIndexRetriever(
            index=self.index.index,
            similarity_top_k=top_k,
        )
        response_synthesizer = get_response_synthesizer()
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[self.reranker.reranker],
        )

        return query_engine.query(query)

        