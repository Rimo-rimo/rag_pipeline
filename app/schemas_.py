# Pydantic 모델 (요청 및 응답 스키마 정의)

from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class RetrieveType(str, Enum):
    VECTOR_SEARCH = "vector_search"
    BM25_SEARCH = "bm25_search"
    HYBRID_SEARCH = "hybrid_search"

class InsertRequest(BaseModel):
    document_paths: List[str] = Field(
        description="VectorDB에 주입할 문서 경로 리스트",
        example=["document_1.txt", "document_2.pdf", "document_3.hwp"]
    )

class InsertResponse(BaseModel):
    inserted_info: Dict[str, Dict[str, int]] = Field(
        description="VectorDB에 주입된 요소 정보",
        example={"document_1.txt":{"nodes":773},
                 "document_2.pdf":{"nodes":483}}
    )

    collection_num_entities: int = Field(
        description="VectorDB 컬렉션에 저장된 entities(nodes) 개수",
        example=1024
    )

class DeleteRequest(BaseModel):
    pass

class DeleteResponse(BaseModel):
    pass

class RetrieveRequest(BaseModel):
    query: str = Field(
        description="사용자의 검색 쿼리",
        example="rimo가 뭐야?"
    )
    retrieve_type: RetrieveType = Field(
        description="검색 알고리즘 종류",
        example=RetrieveType.VECTOR_SEARCH
    )
    is_rerank: bool = Field(
        description="리랭킹 단계 적용 여부",
        example=True
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
                 'last_modified_date': '2024-09-04',
                 'vector_search_score': 0.54}
    )

    text: str = Field(
        description="node의 text",
        example="rimo는 marimo라는 해양 생물로 부터 따온 이름이다."
    )

class RetrieveResponse(BaseModel):
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
                    'last_modified_date': '2024-09-04',
                    'vector_search_score': 0.54
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
                    'last_modified_date': '2024-09-03',
                    'vector_search_score': 0.67
                },
                "text": "코나는 현대자동차의 전기 SUV 모델이다."
            }
        ]
    )