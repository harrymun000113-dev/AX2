import streamlit as st
st.set_page_config(page_title="YEYAK APP", page_icon="✈️")


# 사이드 바
menu = st.sidebar.radio("메뉴", ["홈","미국","중국","일본"])

if menu == "홈":
    대한민국
    대한민국 설명

elif menu == "미국":
    미국
    미국 설명
    링크 버튼 (미국여행공식사이트 방문)