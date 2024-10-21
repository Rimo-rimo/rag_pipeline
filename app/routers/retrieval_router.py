from fastapi import APIRouter, HTTPException, Depends
from app.services.retrieval_service import RetrievalService
from app.schemas import RetrievalRequest, RetrievalResponse, NodeResponse
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings
from llama_index.core.schema import NodeRelationship  

router = APIRouter()

@router.post("/retrieve_documents", response_model=RetrievalResponse)
def retrieve_documents(request: RetrievalRequest,
                       instance_manager: InstanceManager = Depends(get_instance_manager)):
    try:
        if request.embed_model == "openai":
            retrieval_service = RetrievalService(
                embed_model=instance_manager.openai_embed_model,
                embed_dim=instance_manager.openai_embed_dim,
                reranker=instance_manager.reranker,
                collection_name=request.collection_name,
                milvus_uri=settings.milvus_vector_store_uri
            )
        elif request.embed_model == "bgem3":
            retrieval_service = RetrievalService(
                embed_model=instance_manager.bgem3_embed_model,
                embed_dim=instance_manager.bgem3_embed_dim,
                reranker=instance_manager.reranker,
                collection_name=request.collection_name,
                milvus_uri=settings.milvus_vector_store_uri
            )
            
        retrieved_nodes = retrieval_service.retrieve(request)

        # NodeWithScore 객체를 NodeResponse 객체로 변환
        nodes = []
        for nws in retrieved_nodes:
            node = nws.node
            metadata = node.metadata
            node_response = NodeResponse(
                id=node.id_,
                metadata=metadata,
                text=node.text
            )
            nodes.append(node_response)

        return RetrievalResponse(nodes=nodes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/retrieve_metadata", response_model=RetrievalMetadataResponse)
# def retrieve_documents(request: RetrievalRequest,
#                        instance_manager: InstanceManager = Depends(get_instance_manager)):
#     try:
#         retrieval_service = RetrievalService(
#             embed_model=instance_manager.embed_model,
#             reranker=instance_manager.reranker,
#             embed_dim=instance_manager.embed_dim,
#             collection_name=request.collection_name,
#             milvus_uri=settings.milvus_vector_store_uri
#         )

#         retrieved_nodes = retrieval_service.retrieve(request)

#         # NodeWithScore 객체를 NodeResponse 객체로 변환
#         nodes = []
#         for node in retrieved_nodes:
#             if "file_name" in node.metadata and "page_label" in node.metadata:
#                 node.append({
#                     "file_name":node.metadata["file_name"],
#                     "page_label":node.metadata["page_label"]
#                 })
#             else:
#                 node.append({
#                     "web_link":node.node.relationships[NodeRelationship.SOURCE].node_id
#                 })

#         return RetrievalMetadataResponse(nodes=nodes)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# for node in result_nodes:
#     if "file_name" in node.metadata and "page_label" in node.metadata:
#         print(node.metadata["file_name"], node.metadata["page_label"])
#     else:
#         print(node.node.relationships[NodeRelationship.SOURCE].node_id)
    