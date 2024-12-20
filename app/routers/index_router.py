from fastapi import APIRouter, HTTPException, Depends
from app.services.index_service import IndexService
from app.schemas import InsertRequest, DeleteRequest, InsertResponse, DeleteResponse 
from app.instance_manager import get_instance_manager, InstanceManager
from app.config import settings


router = APIRouter()

@router.post("/insert_documents", response_model=InsertResponse)
def insert_documents(request: InsertRequest,
                     instance_manager: InstanceManager = Depends(get_instance_manager)):
    try:
        if request.embed_model == "openai":
            index_service = IndexService(
                embed_model=instance_manager.openai_embed_model,
                embed_dim=instance_manager.openai_embed_dim,
                collection_name=request.collection_name,
                milvus_uri=settings.milvus_vector_store_uri
            )
        elif request.embed_model == "bgem3":
            index_service = IndexService(
                embed_model=instance_manager.bgem3_embed_model,
                embed_dim=instance_manager.bgem3_embed_dim,
                collection_name=request.collection_name,
                milvus_uri=settings.milvus_vector_store_uri
            )

        inserted_nodes = index_service.insert_documents(request)

        return InsertResponse(
            inserted_nodes_num=len(inserted_nodes),
            collection_row_num=index_service.get_num_entities()    
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))