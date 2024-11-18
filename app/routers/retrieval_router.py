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
            # minimum_score보다 낮은 score를 가진 노드는 건너뜀
            if hasattr(request, 'minimum_score') and nws.score < request.minimum_score:
                continue
                
            node = nws.node
            metadata = node.metadata
            node_response = NodeResponse(
                id=node.id_,
                metadata=metadata,    
                text=node.text,
                score=nws.score
            )
            nodes.append(node_response)

        return RetrievalResponse(nodes=nodes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    