from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter

def document_loader(document_paths: list):
    # 문서들을 로드
    documents = SimpleDirectoryReader(input_files=document_paths).load_data() # recursive를 True로 함으로써, 하위 파일까지 모두 로드
    return documents


def text_splitter(documents, chunk_size: int=1024, chunk_overlap: int=200):

    # 텍스트를 문장 단위로 분할하는 parser 정의
    parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # 로드된 문서들을 parser로 분할 -> 단위 : 노드
    nodes = parser.get_nodes_from_documents(documents)

    return nodes