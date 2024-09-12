##############################################
# Milvus Vecto Store 데이터베이스 연결 및 인덱스 생성
##############################################

from app.config import settings
from app.rag_core.index_storage import IndexStorage

index = None

# index 인스턴스 초기화 함수
def init_index(milvus_uri, collection_name, embed_model):
    global index
    try:
        index = IndexStorage(
            milvus_uri=milvus_uri, 
            collection_name=collection_name, 
            embed_model=embed_model
        )
        print("IndexStorage successfully initialized.")
    except Exception as e:
        print(f"Failed to initialize IndexStorage: {e}")
        raise

# 인덱스 인스턴스 반환 함수
def get_index() -> IndexStorage:
    global index
    if index is None:
        init_index()
    try:
        # 연결 상태 체크 추가
        return index
    except Exception as e:
        print(f"Index connection lost, reinitializing: {e}")
        init_index()
        return index

# index 인스턴스 초기화
init_index(milvus_uri=settings.milvus_vector_store_uri,
           collection_name=settings.collection_name,
           embed_model=settings.embedding_model_default)
