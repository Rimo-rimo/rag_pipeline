from fastapi import APIRouter, HTTPException, Depends
from app.services.retrieval_service import RetrievalService
from app.schemas import RetrievalRequest, RetrievalResponse, NodeResponse, Metadata
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings
from collections import defaultdict
import logging

router = APIRouter()

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



# @router.post("/retrieve_documents", response_model=RetrievalResponse)
# def retrieve_documents(
#     request: RetrievalRequest,
#     instance_manager: InstanceManager = Depends(get_instance_manager)
# ):
#     try:
#         # RetrievalService 생성
#         retrieval_service = RetrievalService(
#             embed_model=getattr(instance_manager, f"{request.embed_model}_embed_model"),
#             embed_dim=getattr(instance_manager, f"{request.embed_model}_embed_dim"),
#             reranker=instance_manager.reranker,
#             collection_name=request.collection_name,
#             milvus_uri=settings.milvus_vector_store_uri
#         )

#         # 검색 수행
#         retrieved_nodes = retrieval_service.retrieve(request)

#         # 문서별로 노드 그룹화 (file_path 또는 url 기준)
#         documents_dict = defaultdict(list)
#         for nws in retrieved_nodes:
#             if request.minimum_score is not None and nws.score < request.minimum_score:
#                 continue
            
#             document_key = nws.node.metadata.get("file_path") or nws.node.metadata.get("url")
#             if not document_key:
#                 logging.warning(f"file_path 또는 url이 없는 노드가 건너뛰어졌습니다. Node ID: {nws.node.id_}")
#                 continue
            
#             documents_dict[document_key].append(nws)
        
#         # documents 생성
#         documents = []
#         for document_key, node_list in documents_dict.items():
#             metadata = create_metadata(node_list[0].node.metadata)
#             nodes = [
#                 NodeResponse(
#                     id=nws.node.id_,  # `id_`는 LlamaIndex 노드 객체의 ID 속성
#                     text=nws.node.text,
#                     page_label=nws.node.metadata.get("page_label"),
#                     score=nws.score
#                 )
#                 for nws in node_list
#             ]
#             documents.append({"metadata": metadata, "nodes": nodes})
        
#         # 응답 데이터 구성
#         response_data = {
#             "documents": documents,
#             "total_documents": len(documents),
#             "total_nodes": sum(len(node_list) for node_list in documents_dict.values())
#         }
        
#         return RetrievalResponse(
#             message="검색 결과를 성공적으로 반환했습니다.",
#             data=response_data
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve_documents", response_model=RetrievalResponse)
def retrieve_documents(
    request: RetrievalRequest,
    instance_manager: InstanceManager = Depends(get_instance_manager)
):
    try:
        # RetrievalService 생성
        retrieval_service = RetrievalService(
            embed_model=getattr(instance_manager, f"{request.embed_model}_embed_model"),
            embed_dim=getattr(instance_manager, f"{request.embed_model}_embed_dim"),
            reranker=instance_manager.reranker,
            collection_name=request.collection_name,
            milvus_uri=settings.milvus_vector_store_uri
        )

        # 검색 수행
        retrieved_nodes = retrieval_service.retrieve(request)

        # 문서별로 노드 그룹화 (file_path 또는 url 기준)
        documents_dict = defaultdict(list)
        for nws in retrieved_nodes:
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
            "total_nodes": sum(len(node_list) for node_list in documents_dict.values())
        }
        
        return RetrievalResponse(
            message="검색 결과를 성공적으로 반환했습니다.",
            data=response_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
