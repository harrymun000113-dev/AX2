import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 1. 상위 폴더 경로와 .env 파일 경로를 정확히 결합합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))  # C:\Users\user\AX2\API
parent_dir = os.path.dirname(current_dir)                 # C:\Users\user\AX2
env_path = os.path.join(parent_dir, '.env')                 # C:\Users\user\AX2\.env

# 지정한 경로의 .env 파일을 명시적으로 불러옵니다.
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 페이지 기본 설정 (반응형 레이아웃 적용)
st.set_page_config(
    page_title="실시간 날씨 조회 앱",
    page_icon="🌤️",
    layout="centered"
)

# 2. 날씨 데이터를 가져오는 함수
def get_weather(city_name):
    if not API_KEY:
        st.error(f"⚠️ API 키가 설정되지 않았습니다. 파일 경로 확인: {env_path}")
        return None
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 온도 사용
        "lang": "kr"        # 한국어 날씨 설명
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning(f"🔍 '{city_name}' 도시를 찾을 수 없습니다. 올바른 영문 도시명을 입력해주세요.")
        else:
            st.error(f"❌ API 오류 발생 (상태 코드: {response.status_code})")
        return None
    except Exception as e:
        st.error(f"🔌 서버 연결 중 오류가 발생했습니다: {e}")
        return None

# 3. UI 화면 구성 (반응형 디자인)
st.title("🌤️ 실시간 날씨 확인 서비스")
st.markdown("상위 폴더의 환경변수(`.env`)와 연동된 OpenWeatherMap 날씨 조회 웹 앱입니다.")

# 사용자 입력 (도시 이름)
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("도시 이름 (영문)", "Seoul", placeholder="예: Seoul, Tokyo, New York")
with col2:
    st.markdown("<br>", unsafe_allow_html=True) # 줄바꿈 정렬
    search_button = st.button("날씨 검색", use_container_width=True)

# 검색 버튼을 누르거나 엔터를 쳤을 때 동작
if search_button or city:
    with st.spinner("날씨 정보를 불러오는 중..."):
        weather_data = get_weather(city)
        
        if weather_data:
            # 데이터 추출
            city_name = weather_data.get("name")
            country = weather_data["sys"].get("country")
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]
            wind_speed = weather_data["wind"]["speed"]
            
            # 결과 출력 영역
            st.markdown("---")
            st.subheader(f"📍 {city_name}, {country}의 날씨 정보")
            
            # 반응형 메트릭 카드 컴포넌트 활용
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("현재 온도", f"{temp}°C", f"체감 {feels_like}°C")
            m_col2.metric("습도", f"{humidity}%")
            m_col3.metric("풍속", f"{wind_speed} m/s")
            
            # 날씨 상태 코멘트
            st.info(f"✨ **상태 요약:** 하늘 상태는 **{description}**입니다.")
            
            # 지도 시각화 (선택사항: 도시 좌표 기반)
            lat = weather_data["coord"]["lat"]
            lon = weather_data["coord"]["lon"]
            
            import pandas as pd
            map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
            st.map(map_data, zoom=10, use_container_width=True)