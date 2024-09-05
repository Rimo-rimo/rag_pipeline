import dotenv
import os
dotenv.load_dotenv()

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding


def bgem3_model():
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3"
    )
    return embed_model

def openai_model():
    embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    return embed_model

def get_milvus_vector_store(collection_name: str):
    vector_store = MilvusVectorStore(
        uri=os.getenv("MILVUS_VECTOR_STORE_URI"), 
        collection_name = collection_name,
        overwrite=False
    )
    return vector_store

def create_milvus_vector_store(collection_name: str, dim: int):
    vector_store = MilvusVectorStore(
        uri=os.getenv("MILVUS_VECTOR_STORE_URI"), 
        collection_name = collection_name,
        overwrite=False,
        dim = dim
    )
    return vector_store

def get_index(vector_store, embed_model):
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model = embed_model, show_progress=True)
    return index


def insert_node(index, nodes):
    index.insert_nodes(nodes, show_progress=True)