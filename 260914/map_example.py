import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🗺️ 서울 주요 명소 지도")

# 1. 서울 시내 명소 4곳의 샘플 데이터
landmarks = [
    {"name": "경복궁", "lat": 37.579617, "lng": 126.977041},
    {"name": "N서울타워", "lat": 37.551169, "lng": 126.988227},
    {"name": "명동거리", "lat": 37.563576, "lng": 126.984603},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566524, "lng": 127.009223}
]

# 2. 지도의 시작 중심 좌표 설정 (서울시청 기준)
seoul_city_hall = [37.5665, 126.9780]

# 3. folium 지도 객체 생성
seoul_map = folium.Map(location=seoul_city_hall, zoom_start=13)

# 4. 지도 위에 마커 추가
for place in landmarks:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], max_width=200),
        tooltip=place["name"]
    ).add_to(seoul_map)

# 5. 스트림릿 화면에 지도 렌더링 (HTML 저장 대신 사용)
st_folium(seoul_map, width=700, height=500)