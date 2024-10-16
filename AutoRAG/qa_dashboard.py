import pandas as pd
import streamlit as st
from utils.qa_gen import gen_query_answer

# query, answer 재생성
def generation(corpus):
    response = gen_query_answer(corpus)
    query = response['query']
    answer = response['answer']
    return query, answer

# Setting
st.set_page_config(
    page_title="QA Check",
    page_icon="✔️",  
    layout="wide")

# Data Path 
qa_path = './results/qa/nursing/nursing_qa.parquet'
corpus_path = './results/qa/nursing/corpus.parquet'

# Data Load
qa_df = pd.read_parquet(qa_path)
corpus_df = pd.read_parquet(corpus_path)
max_idx = len(qa_df) - 1

# Session State for idx
if 'idx' not in st.session_state:
    st.session_state.idx = 0

# Title
st.markdown("<h1 style='text-align: center; color:#5F5F5F;'>QA Check</h1>", unsafe_allow_html=True)

# Gage Bar (sync with idx)
st.session_state.idx = st.slider("idx", 0, max_idx, st.session_state.idx, label_visibility="collapsed")

# Query & Answer Window
query = qa_df.loc[st.session_state.idx, 'query']
answer = qa_df.loc[st.session_state.idx, 'generation_gt']
corpus = corpus_df[corpus_df["doc_id"] == qa_df.loc[st.session_state.idx, "retrieval_gt"][0][0]]["contents"].item()

corpus_col, qa_col = st.columns([1,2])

with corpus_col:
    st.markdown("<h5 style=color:#5F5F5F;'>Corpus</h5>", unsafe_allow_html=True)
    with st.container(border=True):
        st.components.v1.html(corpus, height=472, scrolling=True)

with qa_col:
    st.markdown("<h5 style=color:#5F5F5F;'>Query</h5>", unsafe_allow_html=True)
    new_query = st.text_area("query",query, label_visibility="collapsed", height=50)

    st.markdown("<h5 style=color:#5F5F5F;'>Answer</h5>", unsafe_allow_html=True)
    new_answer = st.text_area("query",answer[0], label_visibility="collapsed", height=300)

    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
    with col1:
        if st.button("이전", use_container_width=True) and st.session_state.idx > 0:
            st.session_state.idx -= 1
            st.rerun()
    with col5:
        if st.button("다음", use_container_width=True) and st.session_state.idx < max_idx:
            st.session_state.idx += 1
            st.rerun()
    with col2:
        if st.button("삭제", use_container_width=True, type="primary"):
            qa_df.drop(st.session_state.idx, inplace=True)
            qa_df.reset_index(drop=True, inplace=True)
            qa_df.to_parquet(qa_path)
            st.toast('Deleted!', icon='🚀')
            st.rerun()
         
    with col3:
        if st.button("Re Generation", use_container_width=True, type="primary"):
            with st.spinner('재생성 중입니다..'):
                new_query, new_answer = generation(corpus)
                qa_df.loc[st.session_state.idx, 'query'] = new_query
                qa_df.loc[st.session_state.idx, 'generation_gt'] = [new_answer]
                qa_df.to_parquet(qa_path)
                st.toast('Generated!', icon='🚀')
                st.rerun()
    with col4:
        if st.button("Save & Next", use_container_width=True, type="primary"):
            qa_df.loc[st.session_state.idx, 'query'] = new_query
            qa_df.loc[st.session_state.idx, 'generation_gt'] = [new_answer]
            qa_df.to_parquet(qa_path)
            st.session_state.idx += 1
            st.toast('Saved!', icon='🚀')
            st.rerun()