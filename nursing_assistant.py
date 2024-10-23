import streamlit as st
import streamlit_scrollable_textbox as stx
import requests
import json
import ast
from collections import defaultdict
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# streamlit run chat_ui.py --server.port 18502 --server.address 0.0.0.0

st.set_page_config(layout="wide")

# pdf_images = defaultdict(list)
# pdf_images["14장 호흡기장애 대상자 간호-(1)"] = convert_from_path("./AutoRAG/data/nursing/14장 호흡기장애 대상자 간호-(1).pdf", dpi=300)[:5]

if 'idx' not in st.session_state:
    st.session_state.idx = 0

def chat_request(query, collection_name, top_n, is_rerank):
    url = "http://localhost:9092/api/chat/query"
    data = { 
        "query": query,
        "collection_name": collection_name,
        "top_n": top_n,
        "is_rerank": is_rerank,
        "embed_model": "bgem3"
    } 
    response = requests.post(url, json=data)
    return response.json()

def test_request(query, collection_name, top_n, is_rerank):
    url = "http://localhost:9092/api/chat/query"
    data = { 
        "query": query,
        "collection_name": collection_name,
        "top_n": top_n,
        "is_rerank": is_rerank,
        "embed_model": "bgem3",
        "prompt_template": "nursing"
    } 
    response = requests.post(url, json=data)
    return response.json()

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

tab1, tab2, tab3 = st.tabs(["Chat", "Test", "hi"])
with tab1:
    with st.sidebar:
        collection_name  = "nursing_html_bgem3"
        # if collection_name == "santa_openai_origin_1024":
        #     st.image("/home/livin/rag_pipeline/images/santa.png")
        # else:
        #     st.image("/home/livin/rag_pipeline/images/heart.png")

        top_n = st.slider("top N", 1, 50, 14)

        is_rerank = st.checkbox("Rerank", True)

    col1, col2 = st.columns([6,4])

    with col1:
        st.markdown("<h1 style='text-align: center;'>Nursing Assistant</h1>", unsafe_allow_html=True)
        query = st.chat_input("간호학에 대해서 궁금한게 있으신가요?")

        if query:
            with st.chat_message("user"):
                st.write(query)
            with st.chat_message("assistant"):
                with st.spinner(text="AI가 문서를 살펴보는 중입니다.."):
                    response = chat_request(query=query, collection_name=collection_name, top_n=int(top_n), is_rerank=is_rerank)
                    with st.container(border=True):
                        st.markdown(response["response"])

    with col2:
        if query:
            st.markdown("<h1 style='text-align: center;'>참고 자료</h1>", unsafe_allow_html=True)
            with st.container(border=True):
                for n, node in enumerate(response["nodes"]):
                    if "file_name" in node["metadata"].keys():
                        st.markdown(f'**:blue[{node["metadata"]["file_name"].split(".")[0]}]** 문서 일부')
                    else:
                        st.markdown(f'**:blue[교육 자료의 링크]** 일부')
                    with st.container(border=True):
                        st.components.v1.html(node["text"], height=300, scrolling=True)

with tab2:
    with open("/home/livin/rag_pipeline/data/nursing_test_1.json", "r") as f:
        test_data = json.load(f)
    
    test_col, reference_col = st.columns([1,1])

    with test_col:
        st.markdown("<h3 style='text-align: center;'>간호학 문제</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(test_data["문제"][st.session_state.idx], unsafe_allow_html=True)
            prev_button, generation_button, next_button = st.columns([1,3,1])
            if generation_button.button("답변 재 생성", use_container_width=True, type="primary"):
                with st.spinner("AI가 문제를 푸는 중입니다.."):
                    response = test_request(query=test_data["문제"][st.session_state.idx], collection_name="nursing_html_bgem3", top_n=14, is_rerank=True)
                    result = ast.literal_eval(response["response"])
                    answer = result["answer"]
                    commentary = result["commentary"]
                    test_data["답변"][st.session_state.idx] = answer
                    test_data["해설"][st.session_state.idx] = commentary
                    test_data["참고자료"][st.session_state.idx] = response["nodes"]
                    # json 파일 저장하기
                    with open("/home/livin/rag_pipeline/data/nursing_test_1.json", "w") as f:
                        json.dump(test_data, f, ensure_ascii=False, indent="\t")
                    st.rerun()
            if prev_button.button("이전", use_container_width=True) and st.session_state.idx > 0:
                st.session_state.idx -= 1
                st.rerun()
            if next_button.button("다음", use_container_width=True) and st.session_state.idx < len(test_data["문제"])-1:
                st.session_state.idx += 1
                st.rerun()
        with st.container(border=True):
            st.markdown("### 답변")
            st.markdown(test_data["답변"][st.session_state.idx], unsafe_allow_html=True)
            st.markdown("### 해설")
            st.markdown(test_data["해설"][st.session_state.idx], unsafe_allow_html=True)

    with reference_col:
        # with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>참고 자료</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            try:
                for n, node in enumerate(test_data["참고자료"][st.session_state.idx]):
                    if "file_name" in node["metadata"].keys():
                        st.markdown(f'**:blue[{node["metadata"]["file_name"].split(".")[0]}]** 문서 일부')
                    else:
                        st.markdown(f'**:blue[교육 자료의 링크]** 일부')
                    with st.container(border=True):
                        # st.components.v1.text(node["text"], height=300, scrolling=True)
                        st.text_area(node["text"])
            except:
                st.write("답변을 재 생성 해 주세요")

with tab3:
    st.image(pdf_images["14장 호흡기장애 대상자 간호-(1)"][3], use_column_width=True)