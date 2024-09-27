#######################
# Query & Response
#######################

from app.rag_core.index_storage import get_index
from app.schemas import RetrievalRequest, ChatRequest
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
    
    def query(self, query: str, top_n: int = 10, is_rerank = False):
        retriever = VectorIndexRetriever(
            index=self.index.index,
            similarity_top_k=top_n,
        )
        response_synthesizer = get_response_synthesizer(llm = self.llm)

        new_text_qa_template = (
            "다음은 컨텍스트 정보입니다.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "컨텍스트 정보만을 참고하여, 기존 지식에 의존하지 않고 질문에 답변해 주세요.\n"
            "답변은 꼭 한국어로 해줘야 합니다.\n"
            "답변은 마크다운 형식으로 보기 좋게 생성해 줘야합니다.\n"
            "질문: {query_str}\n"
            "답변: "
        )

        new_refine_templateText = (
            "기존 질문은 다음과 같습니다: {query_str}\n"
            "다음은 질문에 대한 기존의 답변입니다: {existing_answer}\n"
            "아래의 추가 컨텍스트 정보를 바탕으로 기존 답변을 개선할 기회가 있습니다. (필요한 경우에만).\n"
            "------------\n"
            "{context_msg}\n"
            "------------\n"
            "새로운 컨텍스트를 참고하여, 원래 답변을 질문에 더 잘 맞도록 수정해 주세요. 만약 컨텍스트가 유용하지 않다면, 기존 답변을 반환해 주세요.\n"
            "답변은 꼭 한국어로 해줘야 합니다.\n"
            "답변은 마크다운 형식으로 보기 좋게 생성해 줘야합니다.\n"
            "수정된 답변: "
        )

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

        