#############################
# 환경 변수 및 파라미터 세팅
#############################

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import yaml
import os

# 현재 파일의 디렉토리 경로를 기준으로 설정 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일이 위치한 디렉토리
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.yaml")  # settings.yaml의 절대 경로

load_dotenv()

class Settings(BaseSettings):
    # settings.yaml 파일에서 RAG 시스템 관련 설정 불러오기

    # .env 파일에 정의된 환경변수 불러오기
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    milvus_vector_store_uri: str = os.getenv("MILVUS_VECTOR_STORE_URI")
    fastapi_host: str = os.getenv("FASTAPI_HOST")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT"))

    collection_name: str = ""

    chunk_size: int = 0
    chunk_overlap: int = 0

    embedding_model_default: str = " "
    embedding_model_options: list = []

    rerank_model_default: str = ""
    rerank_model_options: list = []

    vector_search_top_k: int = 0
    rerank_top_k: int = 0

    document_directory: str = "sdf"
    device: str = "sd"
    

    # YAML 파일 로드
    def load_yaml_settings(self, file_path: str = SETTINGS_PATH):
        with open(file_path, "r") as file:
            yaml_content = yaml.safe_load(file)
            self.collection_name = yaml_content["vector_store"]["collection_name"]

            self.chunk_size = yaml_content["preprocessor"]["chunk_size"]
            self.chunk_overlap = yaml_content["preprocessor"]["chunk_overlap"]

            self.embedding_model_default = yaml_content["model"]["embedding_model"]["default"]
            self.embedding_model_options = yaml_content["model"]["embedding_model"]["options"]
            self.rerank_model_default = yaml_content["model"]["rerank_model"]["default"]
            self.rerank_model_options = yaml_content["model"]["rerank_model"]["options"]

            self.vector_search_top_k = yaml_content["retrieval"]["vector_search_top_k"]
            self.rerank_top_k = yaml_content["retrieval"]["rerank_top_k"]

            self.document_directory = yaml_content["document_directory"]
            self.device = yaml_content["device"]

# settings 객체 생성 및 YAML 설정 로드
settings = Settings()
settings.load_yaml_settings()