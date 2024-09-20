##########################################################
# VectorDB와 연결된 Index에 문서(노드)를 삽입, 삭제, 수정 하는 service
##########################################################

from app.db import get_index
from app.schemas import InsertRequest
from app.rag_core.index_storage import IndexStorage
from app.rag_core.document_processor import DocumentProcessor

class IndexService:
    def __init__(self,
                 index: IndexStorage,
                 document_processor: DocumentProcessor):
        
        self.index = index
        self.document_processor = document_processor
    
    def insert_documents(self, request: InsertRequest):
        """
        문서를 로드 및 index에 저장하는 메서드
        """
        documents = self.document_processor.load_files(request.document_paths)
        nodes = self.document_processor.split_documents(documents)
        inserted_nodes = self.index.insert(nodes)
    
    def delete_documents(self, request: DeleteRequest):
        pass

    def get_num_entities(self):
        """
        index 내의 entities(nodes)개수 출력
        """
        return index.num_entities()


