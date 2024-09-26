from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from app.schemas import ChatRequest, ChatResponse, NodeResponse
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def chat_query(request: ChatRequest,
                       instance_manager: InstanceManager = Depends(get_instance_manager)):
    # try:
    chat_service = ChatService(
        embed_model=instance_manager.embed_model,
        embed_dim=instance_manager.embed_dim,
        reranker=instance_manager.reranker,
        llm=instance_manager.llm,
        collection_name=request.collection_name
    )

    query = request.query
    response = chat_service.query(query=query, top_n=request.top_n)

    # NodeWithScore 객체를 NodeResponse 객체로 변환
    nodes = []
    for nws in response.source_nodes:
        node = nws.node
        node_response = NodeResponse(
                id=node.id_,
                metadata=node.metadata,
                text=node.text
            )
        nodes.append(node_response)

    return ChatResponse(
        response=response.response,
        nodes=nodes
    )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))