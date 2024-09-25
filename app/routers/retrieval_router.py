from fastapi import APIRouter, HTTPException, Depends
from app.services.retrieval_service import RetrievalService
from app.schemas import RetrievalRequest, RetrievalResponse, NodeResponse
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings

router = APIRouter()

@router.post("/retrieve_documents", response_model=RetrievalResponse)
def retrieve_documents(request: RetrievalRequest,
                       instance_manager: InstanceManager = Depends(get_instance_manager)):
    try:
        retrieval_service = RetrievalService(
            embed_model=instance_manager.embed_model,
            reranker=instance_manager.reranker,
            embed_dim=instance_manager.embed_dim,
            collection_name=request.collection_name,
            milvus_uri=settings.milvus_vector_store_uri
        )

        retrieved_nodes = retrieval_service.retrieve(request)

        # NodeWithScore 객체를 NodeResponse 객체로 변환
        nodes = []
        for nws in retrieved_nodes:
            node = nws.node
            node_response = NodeResponse(
                id=node.id_,
                metadata=node.metadata,
                text=node.text
            )
            nodes.append(node_response)

        return RetrievalResponse(nodes=nodes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))