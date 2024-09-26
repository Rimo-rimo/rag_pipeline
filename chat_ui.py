import streamlit as st
import requests

def chat_request(query, collection_name, top_n, is_rerank):
    url = "http://localhost:9092/api/chat/query"
    data = { 
        "query": query,
        "collection_name": collection_name,
        "top_n": top_n
    }
    response = requests.post(url, json=data)
    return response.json()

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Rag Pipeline</h1>", unsafe_allow_html=True)

with st.sidebar:
    collection_name = st.selectbox(
        "Collection Name",
        ("rag_pipeline", "my_car", "hyundai_MX5_bgeM3_512"),
    )
    top_n = st.slider("top N", 1, 50, 20)
    is_rerank = st.checkbox("Rerank", True)

col1, col2 = st.columns(2)

with col1:
    query = st.chat_input("What is up?")
    if query:
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            with st.spinner(text="In progress..."):
                response = chat_request(query=query, collection_name=collection_name, top_n=int(top_n), is_rerank=is_rerank)
                st.write(response["response"])

with col2:
    if query:
        with st.container(border=True):
            for node in response["nodes"]:
                with st.container(border=True):
                    st.write(node["text"])
