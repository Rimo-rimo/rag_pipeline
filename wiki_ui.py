import streamlit as st
import streamlit_scrollable_textbox as stx
import requests

# streamlit run chat_ui.py --server.port 18502 --server.address 0.0.0.0

st.set_page_config(layout="wide")

def chat_request(query, collection_name, top_n, is_rerank, embed_model):
    url = "http://localhost:9092/api/chat/query"
    data = { 
        "query": query,
        "collection_name": collection_name,
        "top_n": top_n,
        "is_rerank": is_rerank,
        "embed_model" : embed_model
    } 
    response = requests.post(url, json=data)
    return response.json()

# st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
) 

with st.sidebar:
    # collection_name = st.selectbox(
    #     "Collection Name",
    #     ("santa_openai_origin_1024", "HeartOn_openai_origin_1024"),
    # )
    collection_name  =  "wiki_ko_bgem3"
    # if collection_name == "santa_openai_origin_1024":
    #     st.image("/home/livin/rag_pipeline/images/santa.png")
    # else:
    #     st.image("/home/livin/rag_pipeline/images/heart.png")

    top_n = st.slider("top N", 1, 50, 10)

    is_rerank = st.checkbox("Rerank", True)

col1, col2 = st.columns([6,4])

with col1:
    st.markdown("<h1 style='text-align: center;'>위키백과 질의 검색</h1>", unsafe_allow_html=True)
    query = st.chat_input("What is up?")

    if query:
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            with st.spinner(text="AI가 문서를 살펴보는 중입니다.."):
                response = chat_request(query=query, collection_name=collection_name, top_n=int(top_n), is_rerank=is_rerank, embed_model="bgem3")
                with st.container(border=True):
                    st.markdown(response["response"])

with col2:
    if query:
        st.markdown("<h1 style='text-align: center;'>참고한 위키백과</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            for n, node in enumerate(response["nodes"]):
                st.markdown(node["metadata"]["filename"])
                stx.scrollableTextbox(node["text"], key=f"reason_{n}", height=220)
                # st.text(node)
                    
 