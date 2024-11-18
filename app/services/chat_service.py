#######################
# Query & Response
#######################

from app.rag_core.index_storage import get_index
from app.schemas import RetrievalRequest, ChatRequest
from app.utils import prompt_templates
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import PromptTemplate


class ChatService():
    def __init__(self, embed_model, reranker, llm, embed_dim, collection_name: str):
        self.index = get_index(embed_model = embed_model,
                        embed_dim = embed_dim,
                        collection_name = collection_name)

        self.reranker = reranker
        self.llm = llm
    
    def query(self, query: str, top_n: int = 10, is_rerank = False, prompt_template = "basic"):
        retriever = VectorIndexRetriever(
            index=self.index.index, 
            similarity_top_k=top_n,
        )
        response_synthesizer = get_response_synthesizer(llm = self.llm)

        if prompt_template == "basic":
            new_text_qa_template = prompt_templates.basic_text_qa_template
            new_refine_templateText = prompt_templates.basic_refine_template
        elif prompt_template == "nursing":
            new_text_qa_template = prompt_templates.nursing_assistant_test_text_qa_template
            new_refine_templateText = prompt_templates.nursing_assistant_test_refine_template

        new_text_qa_template = PromptTemplate(new_text_qa_template)
        new_refine_templateText = PromptTemplate(new_refine_templateText)

        response_synthesizer.update_prompts(
            {"text_qa_template": new_text_qa_template,
             "refine_template": new_refine_templateText})

        if is_rerank:
            query_engine = RetrieverQueryEngine.from_args(
                retriever=retriever,
                response_synthesizer=response_synthesizer,
                node_postprocessors=[self.reranker.reranker]
            )
        else:
            query_engine = RetrieverQueryEngine.from_args(
                retriever=retriever,
                response_synthesizer=response_synthesizer
            )
        # query_engine = self.index.index.as_query_engine(similarity_top_k=top_n, llm=self.llm)

        # query_engine.update_prompts(
        #     {"response_synthesizer:text_qa_template": new_text_qa_template,
        #     "response_synthesizer:refine_template": new_refine_templateText}
        # )
        return query_engine.query(query)

        