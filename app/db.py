##############################################
# Milvus Vecto Store 데이터베이스 연결 및 인덱스 생성
##############################################

from app.config import settings
from app.rag_pipeline.index_storage import IndexStorage

# Index 생성을 위한 parameter
MILVUS_URI = settings.milvus_vector_store_uri
COLLECTION_NAME = settings.collection_name
EMBEDED_MODEL = settings.embedding_model_default


index = IndexStorage(milvus_uri=MILVUS_URI, 
                     collection_name=COLLECTION_NAME, 
                     embed_model=EMBEDED_MODEL)