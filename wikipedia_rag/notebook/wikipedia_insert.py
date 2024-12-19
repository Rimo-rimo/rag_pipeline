import glob
import pandas as pd
from llama_index.core import Document
from tqdm import tqdm
import os
import sys
import dotenv
dotenv.load_dotenv()
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import logging
from datetime import datetime


from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from pymilvus import Collection, connections
import time

import openai
from llama_index.llms.openai import OpenAI

# 로깅 설정
log_filename = f"wikipedia_insert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # 콘솔에도 출력
    ]
)
logger = logging.getLogger(__name__)

# Setting
dotenv.load_dotenv()
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
vector_store = MilvusVectorStore(
    uri="http://localhost:19530", collection_name = "wiki_ko_bgem3", dim=1024, similarity_metric="COSINE", overwrite=False)
storage_context = StorageContext.from_defaults(vector_store=vector_store)




# 실행
file_path = "/home/livin/rag_pipeline/wikipedia_rag/data/wikipedia/wiki_en.parquet"
df = pd.read_parquet(file_path)
batch_size = 20000

for batch_start in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
    batch_end = min(batch_start + batch_size, len(df))
    batch_df = df.iloc[batch_start:batch_end]
    documents = []
    
    try:
        logger.info(f"Starting batch processing from index {batch_start} to {batch_end}")
        
        for i in range(len(batch_df)):
            document = Document(
                text=batch_df.iloc[i]["text"],
                metadata={"filename": batch_df.iloc[i]["title"], "url": batch_df.iloc[i]["url"]},
            )
            documents.append(document)
        
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
        nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
        index = VectorStoreIndex(nodes, embed_model=embed_model, storage_context=storage_context, show_progress=True)
        
        logger.info(f"Successfully completed batch {batch_start} to {batch_end}")
        
    except Exception as e:
        logger.error(f"Error occurred at batch starting with index {batch_start}: {str(e)}")
        logger.error(f"Last processed document index in this batch: {i}")
        logger.error(f"Last processed document title: {batch_df.iloc[i]['title']}")
        break


    # 메모리 정리를 위해 배치 처리 후 변수들을 명시적으로 삭제
    del documents
    del nodes
    del batch_df




###### 레거시
# documents = []

# for i in tqdm(range(len(df))):
#     document = Document(
#         text=df.iloc[i]["text"],
#         metadata={"filename": df.iloc[i]["title"], "url": df.iloc[i]["url"]},
#     )
#     documents.append(document)
# splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
# nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
# index = VectorStoreIndex(nodes, embed_model=embed_model, storage_context=storage_context, show_progress=True)


