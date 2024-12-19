from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from app.schemas import ChatRequest, ChatResponse, NodeResponse, Metadata
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings
from collections import defaultdict
import logging

router = APIRouter()

# @router.post("/query", response_model=ChatResponse)
# def chat_query(request: ChatRequest,
#                        instance_manager: InstanceManager = Depends(get_instance_manager)):
#     # try:
#     if request.embed_model == "openai":
#         chat_service = ChatService(
#             embed_model=instance_manager.openai_embed_model,
#             embed_dim=instance_manager.openai_embed_dim,
#             reranker=instance_manager.reranker,
#             llm=instance_manager.llm,
#             collection_name=request.collection_name
#         )
#     elif request.embed_model == "bgem3":
#         chat_service = ChatService(
#             embed_model=instance_manager.bgem3_embed_model,
#             embed_dim=instance_manager.bgem3_embed_dim,
#             reranker=instance_manager.reranker,
#             llm=instance_manager.llm,
#             collection_name=request.collection_name
#         )

#     query = request.query
#     response = chat_service.query(query=query, top_n=request.top_n, is_rerank=request.is_rerank, prompt_template=request.prompt_template)

#     # NodeWithScore 객체를 NodeResponse 객체로 변환
#     nodes = []
#     for nws in response.source_nodes:
#         # minimum_score보다 낮은 score를 가진 노드는 건너뜀
#         if hasattr(request, 'minimum_score') and nws.score < request.minimum_score:
#             continue
            
#         node = nws.node
#         file_name = node.metadata.get("file_name")
#         if not file_name:
#             file_name = node.metadata.get("filename")
#         metadata = NodeMetadata(
#             page_label=node.metadata.get("page_label"),
#             file_name=file_name,
#             file_path=node.metadata.get("file_path"),
#             file_type=node.metadata.get("file_type"),
#             file_size=node.metadata.get("file_size"),
#             creation_date=node.metadata.get("creation_date"),
#             last_modified_date=node.metadata.get("last_modified_date"),
#             url = node.metadata.get("url")
#         )
#         node_response = NodeResponse(
#                 id=node.id_,
#                 metadata=metadata,
#                 text=node.text,
#                 score=nws.score,
#                 # file_path=node.metadata["file_path"]
#             )
#         nodes.append(node_response)

#     return ChatResponse(
#         response=response.response,
#         nodes=nodes
#     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


def create_metadata(node_metadata) -> Metadata:
    """노드의 메타데이터를 Metadata 객체로 변환"""
    return Metadata(
        file_name=node_metadata.get("file_name") or node_metadata.get("filename"),
        url=node_metadata.get("url"),
        file_path=node_metadata.get("file_path"),
        file_type=node_metadata.get("file_type"),
        file_size=node_metadata.get("file_size"),
        creation_date=node_metadata.get("creation_date"),
        last_modified_date=node_metadata.get("last_modified_date")
    )

@router.post("/query", response_model=ChatResponse)
def retrieve_documents(
    request: ChatRequest,
    instance_manager: InstanceManager = Depends(get_instance_manager)
):
    try:
        # ChatService 생성
        chat_service = ChatService(
            embed_model=getattr(instance_manager, f"{request.embed_model}_embed_model"),
            embed_dim=getattr(instance_manager, f"{request.embed_model}_embed_dim"),
            reranker=instance_manager.reranker,
            llm=instance_manager.llm,
            collection_name=request.collection_name
        )

        # 쿼리 수행
        query = request.query
        response = chat_service.query(query=query, top_n=request.top_n, is_rerank=request.is_rerank, prompt_template=request.prompt_template)

        # 문서별로 노드 그룹화 (file_path 또는 url 기준)
        documents_dict = defaultdict(list)
        for nws in response.source_nodes:
            if request.minimum_score is not None and nws.score < request.minimum_score:
                continue
            
            document_key = nws.node.metadata.get("file_path") or nws.node.metadata.get("url")
            if not document_key:
                logging.warning(f"file_path 또는 url이 없는 노드가 건너뛰어졌습니다. Node ID: {nws.node.id_}")
                continue
            
            documents_dict[document_key].append(nws)
        
        # documents 생성
        documents = []
        for document_key, node_list in documents_dict.items():
            metadata = create_metadata(node_list[0].node.metadata)
            nodes = [
                NodeResponse(
                    id=nws.node.id_,  # `id_`는 LlamaIndex 노드 객체의 ID 속성
                    text=nws.node.text,
                    page_label=nws.node.metadata.get("page_label"),
                    score=nws.score
                )
                for nws in node_list
            ]
            documents.append({"metadata": metadata, "nodes": nodes})
        
        # 응답 데이터 구성
        response_data = {
            "documents": documents,
            "total_documents": len(documents),
            "total_nodes": sum(len(node_list) for node_list in documents_dict.values()),
            "response": response.response
        }
        
        return ChatResponse(
            message="검색 결과를 성공적으로 반환했습니다.",
            data=response_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
