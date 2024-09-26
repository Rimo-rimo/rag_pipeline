import streamlit as st
import streamlit_scrollable_textbox as stx
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
    collection_name = st.selectbox(
        "Collection Name",
        ("HeartOn_openai_origin_1024", "santa_openai_origin_1024", "santa_openai_origin_512"),
    )
    top_n = st.slider("top N", 1, 50, 20)
    is_rerank = st.checkbox("Rerank", True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h1 style='text-align: center;'>Rag Pipeline</h1>", unsafe_allow_html=True)
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
            for n, node in enumerate(response["nodes"]):
                if node["metadata"]:
                    st.markdown(f'**:blue[{node["metadata"]["file_name"]}]** 문서의 ***:blue[{node["metadata"]["page_label"]}]*** page 일부')
                else:
                    st.markdown(f'**:blue[교육 자료의 링크]** 일부')
                stx.scrollableTextbox(node["text"], key=f"reason_{n}", height=220)
                # st.text(node)
                    
