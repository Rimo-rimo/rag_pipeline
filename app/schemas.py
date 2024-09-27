# Pydantic 모델 (요청 및 응답 스키마 정의)

from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from app.config import settings

class RetrieveType(str, Enum):
    VECTOR_SEARCH = "vector_search"
    BM25_SEARCH = "bm25_search"
    HYBRID_SEARCH = "hybrid_search"

class InsertRequest(BaseModel):
    collection_name: str = Field(
        description="VectorDB에 주입할 컬렉션 이름",
        example="rag_pipeline"
    )
    document_paths: List[str] = Field(
        description="VectorDB에 주입할 문서 경로 리스트",
        example=["./data/hyndai_MX5_HEV.pdf", "./data/hyndai.pdf"]
    )
    chunk_size: int = Field(
        description="문서를 청킹할 크기",
        example=settings.chunk_size
    )
    chunk_overlap: int = Field(
        description="문서 청킹 시 겹치는 부분 크기",
        example=settings.chunk_overlap
    )

class InsertResponse(BaseModel):
    inserted_nodes_num: int = Field(
        description="VectorDB에 주입된 노드 수",
        example=483
    )
    collection_row_num: int = Field(
        description="VectorDB에 주입된 컬렉션의 노드 수",
        example=798
    )

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


class NodeResponse(BaseModel):
    id: str = Field(
        description="node의 id",
        example="b39b8a58-5591-4579-84c2-ad3c17e8beaa"
    )

    metadata: Dict[str, Any] = Field(
        description="node가 가진 metadata",
        example={'page_label': '348',
                 'file_name': 'hyndai_MX5_HEV.pdf',
                 'file_path': '/home/livin/rag_pipeline/data/hyndai_MX5_HEV.pdf',
                 'file_type': 'application/pdf',
                 'file_size': 24920366,
                 'creation_date': '2024-09-04',
                 'last_modified_date': '2024-09-04'}
    )

    text: str = Field(
        description="node의 text",
        example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
    )

class RetrievalRequest(BaseModel):
    collection_name: str = Field(
        description="검색 대상 컬렉션 이름",
        example=settings.collection_name
    )
    query: str = Field(
        description="사용자의 검색 쿼리",
        example="차량의 타이어 스펙을 알려줘"
    )

    top_n: int = Field(
        description="검색 결과 중 상위 n개의 결과만 반환",
        example=20
    )

    is_rerank: bool = Field(
        description="리랭킹 적용 여부",
        example=True
    )

class RetrievalResponse(BaseModel):
    nodes: List[NodeResponse] = Field(
        description="검색된 node들의 리스트",
        example=[
            {
                "id": "b39b8a58-5591-4579-84c2-ad3c17e8beaa",
                "metadata": {
                    'page_label': '348',
                    'file_name': 'hyndai_MX5_HEV.pdf',
                    'file_path': '/home/livin/rag_pipeline/data/hyndai_MX5_HEV.pdf',
                    'file_type': 'application/pdf',
                    'file_size': 24920366,
                    'creation_date': '2024-09-04',
                    'last_modified_date': '2024-09-04'
                },
                "text": "rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
            },
            {
                "id": "d29b1a25-32a7-4a13-a14b-12c4b9e1c7fa",
                "metadata": {
                    'page_label': '123',
                    'file_name': 'hyundai_Kona_EV.pdf',
                    'file_path': '/home/livin/rag_pipeline/data/hyundai_Kona_EV.pdf',
                    'file_type': 'application/pdf',
                    'file_size': 10234567,
                    'creation_date': '2024-09-03',
                    'last_modified_date': '2024-09-03'
                },
                "text": "코나는 현대자동차의 전기 SUV 모델이다."
            }
        ]
    )

class ChatRequest(RetrievalRequest):
    pass

class ChatResponse(RetrievalResponse):
    response: str = Field(
        description="Chatbot의 응답",
        example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
    )

