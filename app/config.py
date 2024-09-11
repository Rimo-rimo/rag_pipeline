#############################
# 환경 변수 및 파라미터 세팅
#############################

from pydantic import BaseSettings
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

class Settings(BaseSettings):

    # .env 파일에 정의된 환경변수 불러오기
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    milvus_vector_store_uri: str = os.getenv("MILVUS_VECTOR_STORE_URI")
    fastapi_host: str = os.getenv("FASTAPI_HOST")
    fastapi_port: int = int(os.getenv("FASTAPT_PORT"))

    # settings.yaml 파일에서 RAG 시스템 관련 설정 불러오기
    collection_name: str

    chunk_size: int
    chunk_overlap: int

    embedding_model_default: str
    embedding_model_options: list

    rerank_model_default: str
    rerank_model_options: list

    vector_search_top_k: int
    rerank_top_k: int

    document_directory: str
    device: str
    

    # YAML 파일 로드
    def load_yaml_settings(self, file_path: str = "app/settings.yaml"):
        with open(file_path, "r") as file:
            yaml_content = yaml.safe_load(file)
            self.collection_name = yaml_content["vector_store"]["collection_name"]

            self.chunk_size = yaml_content["preprocessor"]["chunk_size"]
            self.chunk_overlap = yaml_content["preprocessor"]["chunk_overlap"]

            self.embedding_model_default = yaml_content["model"]["embedding_model"]["default"]
            self.embedding_model_options = yaml_content["model"]["embedding_model"]["options"]
            self.rerank_model_default = yaml_content["model"]["rerank_model"]["default"]
            self.rerank_model_options = yaml_content["model"]["rerank_model"]["options"]

            self.vector_search_top_k = yaml_content["retriever"]["vector_search_top_k"]
            self.rerank_top_k = yaml_content["retriever"]["rerank_top_k"]

            self.document_directory = yaml_content["document_directory"]
            self.device = yaml_content["device"]

# settings 객체 생성 및 YAML 설정 로드
settings = Settings()
settings.load_yaml_settings()