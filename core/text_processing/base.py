from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter


def text_loader(folder_path, chunk_size: int=1024, chunk_overlap: int=200):
    """
    긴 텍스트를 작은 단위의 텍스트 조각으로 분할 하는 함수

    Parameters:
    ----------
    folder_path : str
        문서 파일들이 모여있는 폴더 경로
    chunk_size : int
        각 청크의 최대 사이즈
    chunk_overlap : int
        각 청크 마다 중복으로 겹쳐지는 길이

    Returns:
    -------
    nodes : list of node
        분할된 텍스트 단위인 노드들의 리스트
    """

    # 폴더 내의 문서들을 로드
    documents = SimpleDirectoryReader(input_dir=folder_path, recursive=True).load_data() # recursive를 True로 함으로써, 하위 파일까지 모두 로드

    # 텍스트를 문장 단위로 분할하는 parser 정의
    parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # 로드된 문서들을 parser로 분할 -> 단위 : 노드
    nodes = parser.get_nodes_from_documents(documents)

    return nodes