import streamlit as st

# CSS 스타일 추가 (변수 사용)
st.markdown(
    """
    <style>
    :root {
        --main-color: #4CAF50;  /* 메인 컬러 변수 설정 */
    }

    .stButton>button {
        background-color: var(--main-color);
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
    }

    .stButton>button:hover {
        background-color: var(--main-color);
        opacity: 0.8;  /* hover 시 밝기만 조정하여 동일한 색상 유지 */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# 버튼 생성
if st.button('Custom Button'):
    st.write('버튼을 눌렀습니다!')

st.slider('Slider', 0, 100, 50)  # 슬라이더 생성