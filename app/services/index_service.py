##########################################################
# VectorDB와 연결된 Index에 문서(노드)를 삽입, 삭제, 수정 하는 service
##########################################################

from app.rag_core.index_storage import get_index
from app.schemas import InsertRequest, DeleteRequest
from app.rag_core.index_storage import IndexStorage
from app.rag_core.document_processor import DocumentProcessor

class IndexService:
    def __init__(self, embed_model, embed_dim: int, collection_name: str, milvus_uri: str): 
        
        self.index = get_index(embed_model = embed_model,
                               embed_dim = embed_dim,
                               collection_name = collection_name,
                               milvus_uri = milvus_uri)
    
    def insert_documents(self, request: InsertRequest):
        """
        문서를 로드 및 index에 저장하는 메서드
        """
        self.document_processor = DocumentProcessor(request.chunk_size, request.chunk_overlap)   
        documents = self.document_processor.load_files(request.document_paths)
        nodes = self.document_processor.split_documents(documents)
        inserted_nodes = self.index.insert(nodes)
        return inserted_nodes
    
    def delete_documents(self, request: DeleteRequest):
        """
        문서를 index에서 삭제하는 메서드
        """
        pass

    def get_num_entities(self):
        """
        index 내의 entities(nodes)개수 출력
        """
        return self.index.num_entities()


