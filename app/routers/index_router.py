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
        index_service = IndexService(
            embed_model=instance_manager.embed_model,
            embed_dim=instance_manager.embed_dim,
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

# @router.post("/delete_documents", response_model=DeleteResponse)
# def delete_documents(request: DeleteRequest):
#     try:
#         index_service.delete_documents(request)
#         return {"message": "Documents deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/num_entities")
def get_num_entities():
    try:
        num_entities = index_service.get_num_entities()
        return {"num_entities": num_entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))