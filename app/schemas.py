# # Pydantic 모델 (요청 및 응답 스키마 정의)

# from typing import Union, List, Dict, Any, Optional
# from pydantic import BaseModel, Field
# from enum import Enum
# from app.config import settings
# from typing_extensions import Annotated

# class RetrieveType(str, Enum):
#     VECTOR_SEARCH = "vector_search"
#     BM25_SEARCH = "bm25_search"
#     HYBRID_SEARCH = "hybrid_search"

# class InsertRequest(BaseModel):
#     collection_name: Annotated[str, Field(
#         description="VectorDB에 주입할 컬렉션 이름",
#         example="example_collection"
#     )]
#     document_paths: Annotated[List[str], Field(
#         description="VectorDB에 주입할 문서 경로 리스트",
#         example=["./data/hyndai_MX5_HEV.pdf", "./data/hyndai.pdf"]
#     )]
#     chunk_size: Annotated[int, Field(
#         description="문서를 청킹할 크기",
#         example=1024  # 실제 값으로 대체하세요
#     )]
#     chunk_overlap: Annotated[int, Field(
#         description="문서 청킹 시 겹치는 부분 크기",
#         example=200  # 실제 값으로 대체하세요
#     )]
#     embed_model: Annotated[str, Field(
#         default="bgem3",
#         description="임베딩 모델('openai' or 'bge-m3')",
#         example="bgem3"
#     )]


# class InsertResponse(BaseModel):
#     inserted_nodes_num: int = Field(
#         description="VectorDB에 주입된 노드 수",
#         example=483
#     )
#     collection_row_num: int = Field(
#         description="VectorDB에 주입된 컬렉션의 노드 수",
#         example=798
#     )

# class NodeMetadata(BaseModel):
#     page_label: Optional[str] = Field(
#         default=None,
#         description="문서의 페이지 번호",
#         example="540"
#     )
#     file_name: Optional[str] = Field(
#         default=None,
#         description="파일 이름",
#         example="test.pdf"
#     )
#     url: Optional[str] = Field(
#         default=None,
#         description="문서 링크",
#         example="test.com"
#     )
#     file_path: Optional[str] = Field(
#         default=None,
#         description="파일 경로",
#         example="/data/sub/test.pdf"
#     )
#     file_type: Optional[str] = Field(
#         default=None,
#         description="파일 타입",
#         example="application/pdf"
#     )
#     file_size: Optional[int] = Field(
#         default=None,
#         description="파일 크기(bytes)",
#         example=24920366
#     )
#     creation_date: Optional[str] = Field(
#         default=None,
#         description="파일 생성일",
#         example="2024-09-04"
#     )
#     last_modified_date: Optional[str] = Field(
#         default=None,
#         description="파일 수정일",
#         example="2024-09-04"
#     )

# class NodeResponse(BaseModel):
#     id: str = Field(
#         description="node의 id",
#         example="b39b8a58-5591-4579-84c2-ad3c17e8beaa"
#     )
#     metadata: NodeMetadata = Field(
#         description="node가 가진 metadata"
#     )
#     text: str = Field(
#         description="node의 text",
#         example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
#     )
#     score: float = Field(
#         description="검색 점수",
#         example=0.67
#     )    
    
# class RetrievalRequest(BaseModel):
#     collection_name: str = Field(
#         description="검색 대상 컬렉션 이름",
#         example="wiki_bgem3"
#     )
#     query: str = Field(
#         description="사용자의 검색 쿼리",
#         example="차량의 타이어 스펙을 알려줘"
#     )

#     top_n: int = Field(
#         description="검색 결과 중 상위 n개의 결과만 반환",
#         example=20
#     )

#     is_rerank: bool = Field(
#         description="리랭킹 적용 여부",
#         example=True
#     )

#     embed_model: str = Field(
#         default="bgem3",
#         description="임베딩 모델('openai' or 'bgem3')",
#         example="bgem3"
#     )

#     minimum_score: Optional[float] = Field(default=0.0, description="최소 유사도 점수")
    


# class RetrievalResponse(BaseModel):
#     nodes: List[NodeResponse] = Field(
#         description="검색된 node들의 리스트"
#     )

# class ChatRequest(RetrievalRequest):
#     prompt_template: str = Field(
#         default="basic",
#         description="프롬프트 템플릿",
#         example="basic"
#     )

# class ChatResponse(RetrievalResponse):
#     response: str = Field(
#         description="Chatbot의 응답",
#         example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
#     )

# class DocumentSummaryRequest(BaseModel):
#     file_path: str = Field(
#         description="file_path",
#         example="/data/subfolder/test.pdf"
#     )

# class DocumentSummaryResponse(BaseModel):
#     file_path: str = Field(
#         description="file_path",
#         example="/data/subfolder/test.pdf"
#     )
#     summary: str = Field(
#         description="document의 요약본",
#         example="document의 요약본"
#     )

# class NumEntitiesResponse(BaseModel):
#     num_entities: int = Field(
#         description="청킹된 노드들의 개수",
#         example=239485
#     )    
#     num_documents: int = Field(
#         description="문서의 개수",
#         example=230582
#     )    



# Pydantic 모델 (요청 및 응답 스키마 정의)

from typing import Union, List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from app.config import settings
from typing_extensions import Annotated

# Enum for Retrieve Types
class RetrieveType(str, Enum):
    VECTOR_SEARCH = "vector_search"
    BM25_SEARCH = "bm25_search"
    HYBRID_SEARCH = "hybrid_search"

# Common Base Response Schema
class BaseResponse(BaseModel):
    message: Annotated[str, Field(
        description="응답 메시지",
        example="요청이 성공적으로 처리되었습니다."
    )]
    data: Optional[Union[List[dict], dict]] = Field(
        description="응답 데이터",
        example={}
    )

# Metadata Schema
class Metadata(BaseModel):
    file_name: Optional[str] = Field(
        description="파일 이름",
        example="test_1.pdf"
    )
    url: Optional[str] = Field(
        description="문서 링크",
        example="test_1.com"
    )
    file_path: Optional[str] = Field(
        description="파일 경로",
        example="/data/sub/test_1.pdf"
    )
    file_type: Optional[str] = Field(
        description="파일 타입",
        example="application/pdf"
    )
    file_size: Optional[int] = Field(
        description="파일 크기(bytes)",
        example=24920366
    )
    creation_date: Optional[str] = Field(
        description="파일 생성일",
        example="2024-09-04"
    )
    last_modified_date: Optional[str] = Field(
        description="파일 수정일",
        example="2024-09-04"
    )

# Node Response Schema
class NodeResponse(BaseModel):
    id: str = Field(
        description="node의 id",
        example="b39b8a58-5591-4579-84c2-ad3c17e8beaa"
    )
    text: str = Field(
        description="node의 text",
        example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
    )
    page_label: Optional[str] = Field(
        default=None,
        description="문서의 페이지 번호",
        example="540"
    )
    score: float = Field(
        description="검색 점수",
        example=0.67
    )  

# Insert Request Schema
class InsertRequest(BaseModel):
    collection_name: Annotated[str, Field(
        description="VectorDB에 주입할 컬렉션 이름",
        example="example_collection"
    )]
    document_paths: Annotated[List[str], Field(
        description="VectorDB에 주입할 문서 경로 리스트",
        example=["./data/hyndai_MX5_HEV.pdf", "./data/hyndai.pdf"]
    )]
    chunk_size: Annotated[int, Field(
        description="문서를 청킹할 크기",
        example=1024  # 실제 값으로 대체하세요
    )]
    chunk_overlap: Annotated[int, Field(
        description="문서 청킹 시 겹치는 부분 크기",
        example=200  # 실제 값으로 대체하세요
    )]
    embed_model: Annotated[str, Field(
        default="bgem3",
        description="임베딩 모델('openai' or 'bge-m3')",
        example="bgem3"
    )]

# Insert Response Schema
class InsertResponse(BaseResponse):
    class Data(BaseModel):
        inserted_nodes_num: int = Field(
            description="VectorDB에 주입된 노드 수",
            example=483
        )
        collection_row_num: int = Field(
            description="VectorDB에 주입된 컬렉션의 노드 수",
            example=798
        )
    data: Data

class DeleteRequest(BaseModel):
    collection_name: str = Field(
        description="VectorDB에서 삭제할 컬렉션 이름",
        example=settings.collection_name
    )
    document_paths: List[str] = Field(
        description="VectorDB에서 삭제할 문서 경로 리스트",
        example=["document_1.txt", "document_2.pdf"]
    )

class DeleteResponse(BaseModel):
    deleted_nodes_num: int = Field(
        description="VectorDB에서 삭제된 노드 수",
        example=483
    )
    collection_row_num: int = Field(
        description="VectorDB에서 삭제된 컬렉션의 노드 수",
        example=798
    )
    
# Retrieval Request Schema
class RetrievalRequest(BaseModel):
    collection_name: Annotated[str, Field(
        description="검색 대상 컬렉션 이름",
        example="wiki_bgem3"
    )]
    query: Annotated[str, Field(
        description="사용자의 검색 쿼리",
        example="차량의 타이어 스펙을 알려줘"
    )]
    top_n: Annotated[int, Field(
        description="검색 결과 중 상위 n개의 결과만 반환",
        example=20
    )]
    is_rerank: Annotated[bool, Field(
        description="리랭킹 적용 여부",
        example=True
    )]
    embed_model: Annotated[str, Field(
        default="bgem3",
        description="임베딩 모델('openai' or 'bgem3')",
        example="bgem3"
    )]
    minimum_score: Optional[float] = Field(
        default=0.0,
        description="최소 유사도 점수"
    )

# Retrieval Response Schema
class RetrievalResponse(BaseResponse):
    class Data(BaseModel):
        class Document(BaseModel):
            metadata: Metadata
            nodes: List[NodeResponse]

        documents: List[Document]
        total_documents: int = Field(
            description="검색된 문서의 총 개수",
            example=2
        )
        total_nodes: int = Field(
            description="검색된 노드의 총 개수",
            example=10
        )
    data: Data

# Chat Request Schema
class ChatRequest(RetrievalRequest):
    prompt_template: Annotated[str, Field(
        default="basic",
        description="프롬프트 템플릿",
        example="basic"
    )]

# Chat Response Schema
class ChatResponse(BaseResponse):
    class Data(BaseModel):
        class Document(BaseModel):
            metadata: Metadata
            nodes: List[NodeResponse]

        documents: List[Document]
        total_documents: int = Field(
            description="검색된 문서의 총 개수",
            example=2
        )
        total_nodes: int = Field(
            description="검색된 노드의 총 개수",
            example=10
        )
        response: str = Field(
            description="Chat 응답",
            example="이 문서는 차량의 타이어 스펙에 대해 설명합니다."
        )
    data: Data

class DocumentSummaryRequest(BaseModel):
    file_path: Annotated[str, Field(
        description="file_path",
        example="/data/subfolder/test.pdf"
    )]


# Document Summary Response Schema
class DocumentSummaryResponse(BaseResponse):
    class Data(BaseModel):
        file_path: Annotated[str, Field(
            description="file_path",
            example="/data/subfolder/test.pdf"
        )]
        summary: Annotated[str, Field(
            description="document의 요약본",
            example="document의 요약본"
        )]
    data: Data

# Num Entities Response Schema
class NumEntitiesResponse(BaseResponse):
    class Data(BaseModel):
        num_entities: Annotated[int, Field(
            description="청킹된 노드들의 개수",
            example=239485
        )]
        num_documents: Annotated[int, Field(
            description="문서의 개수",
            example=230582
        )]
    data: Data  