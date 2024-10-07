import streamlit as st

with open("./parsed_data/hyundai.html", "r", encoding="utf-8") as file:
    html_content = file.read()

st.html(html_content)