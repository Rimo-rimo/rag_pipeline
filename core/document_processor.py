from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter

class DocumentProcessor():
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.parser = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def load_files(self, document_paths: list):
        """
        - 파일을 텍스트 형태로 추출하여, 라마인덱스의 Document 요소로 변환

        Args:
            document_paths (list) : 로드할 문서 경로들의 리스트
            
        Returns:
            documents (list) : 라마인덱스의 Documents 클래스의 리스트
        """
        try:
            documents = SimpleDirectoryReader(input_files=document_paths).load_data()
            print(f"Loaded {len(documents)} documents.")
            return documents
        except Exception as e:
            print(f"Error loading documents: {e}")
            raise
        return documents

    def split_documents(documents):
        """
        - 로드된 문서를 청킹하여 라마인덱스의 노드 단위로 분할

        Args:
            documents (list) : 로드된 document 객체의 리스트

        Returns 
            nodes (list) : 분할된 노드 객체의 리스트
        """
        try:
            nodes = self.parser.get_nodes_from_documents(documents)
            print(f"Split documents into {len(nodes)} nodes.")
            return nodes
        except Exception as e:
            print(f"Error splitting text: {e}")
            raise