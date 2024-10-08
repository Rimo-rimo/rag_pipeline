import warnings
warnings.filterwarnings(action='ignore')
import os
import sys
import dotenv
import nest_asyncio
dotenv.load_dotenv()

from autorag.evaluator import Evaluator

evaluator = Evaluator(
    qa_data_path='./results/qa/hyundai_upstage_qa_all.parquet', 
    corpus_data_path='./results/qa/hyundai_upstage_corpus.parquet')
evaluator.start_trial('./auto_rag_ko_example.yaml')