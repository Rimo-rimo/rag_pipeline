from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from app.schemas import ChatRequest, ChatResponse, NodeResponse, NodeMetadata
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def chat_query(request: ChatRequest,
                       instance_manager: InstanceManager = Depends(get_instance_manager)):
    # try:
    if request.embed_model == "openai":
        chat_service = ChatService(
            embed_model=instance_manager.openai_embed_model,
            embed_dim=instance_manager.openai_embed_dim,
            reranker=instance_manager.reranker,
            llm=instance_manager.llm,
            collection_name=request.collection_name
        )
    elif request.embed_model == "bgem3":
        chat_service = ChatService(
            embed_model=instance_manager.bgem3_embed_model,
            embed_dim=instance_manager.bgem3_embed_dim,
            reranker=instance_manager.reranker,
            llm=instance_manager.llm,
            collection_name=request.collection_name
        )

    query = request.query
    response = chat_service.query(query=query, top_n=request.top_n, is_rerank=request.is_rerank, prompt_template=request.prompt_template)

    # NodeWithScore 객체를 NodeResponse 객체로 변환
    nodes = []
    for nws in response.source_nodes:
        # minimum_score보다 낮은 score를 가진 노드는 건너뜀
        if hasattr(request, 'minimum_score') and nws.score < request.minimum_score:
            continue
            
        node = nws.node
        metadata = NodeMetadata(
            page_label=node.metadata.get("page_label"),
            file_name=node.metadata.get("file_name"),
            file_path=node.metadata.get("file_path"),
            file_type=node.metadata.get("file_type"),
            file_size=node.metadata.get("file_size"),
            creation_date=node.metadata.get("creation_date"),
            last_modified_date=node.metadata.get("last_modified_date")
        )
        node_response = NodeResponse(
                id=node.id_,
                metadata=metadata,
                text=node.text,
                score=nws.score,
                # file_path=node.metadata["file_path"]
            )
        nodes.append(node_response)

    return ChatResponse(
        response=response.response,
        nodes=nodes
    )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

