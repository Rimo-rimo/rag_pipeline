from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas import NumEntitiesResponse
from app.config import settings
from pymilvus import Collection
from pymilvus import connections
import os
from urllib.parse import unquote
from glob import glob


router = APIRouter()

@router.get("/statistics", response_model=NumEntitiesResponse)
def get_document_summary(collection_name: str = Query(..., description="Collection Name")):
    try:
        milvus_host, milvus_port = settings.milvus_vector_store_uri.split("/")[-1].split(":")
        
        connections.connect(
            alias="default", 
            host=milvus_host,
            port=milvus_port
            )
        milvus_collection = Collection(name=collection_name)
        
        num_entities = milvus_collection.num_entities
        
        if collection_name == "wiki_bgem3":
            file_paths = [1]*6734237
        else:
            file_paths = [i for i in glob(f"/data/sharedoc/{collection_name}/**", recursive=True) if os.path.isfile(i)]
        
        return NumEntitiesResponse(
            message="응답 결과를 성공적으로 반환했습니다.",
            data= {
                "num_entities": num_entities,
                "num_documents": len(file_paths)
            }
        )
        
    except:
        raise HTTPException(status_code=404, detail="Collection not found")