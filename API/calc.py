import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv, find_dotenv

# 1. 페이지 설정 (가장 먼저 실행되어야 함)
st.set_page_config(
    page_title="Victorian Cabinet Hub",
    page_icon="🕰️",
    layout="wide"
)

# 2. 고급 폰트 및 예술적 CSS 스타일 적용
st.markdown("""
    <style>
    /* Google Fonts 로드 (고급스러운 세리프체) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* 전체 배경을 오래된 양피지 톤으로 설정 */
    .stApp {
        background-color: #EBE5D9;
        font-family: 'Playfair Display', serif;
        color: #2C221E;
    }
    
    /* 상단 기본 헤더 숨김 */
    header { visibility: hidden; }

    /* --- 🖼️ 명화 배너 특수효과 및 스타일 --- */
    .artistic-banner {
        position: relative;
        width: 100%;
        height: 320px;
        overflow: hidden;
        border: 8px solid #3B2F2F; /* 두꺼운 원목 액자 틀 */
        border-radius: 4px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        margin-bottom: 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    /* 명화 배경 (애니메이션 효과 포함) */
    .artistic-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        /* 안정적인 모네 수련 이미지 URL 적용 */
        background-image: url('https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        z-index: 0;
        animation: subtleZoom 10s infinite alternate ease-in-out;
    }

    /* 가독성을 위한 다크 빈티지 오버레이 필름 */
    .artistic-banner::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(25, 15, 10, 0.4), rgba(25, 15, 10, 0.8));
        z-index: 1;
    }

    /* 얇은 내부 금장 테두리 */
    .inner-gold-frame {
        position: absolute;
        top: 15px; left: 15px; right: 15px; bottom: 15px;
        border: 2px solid rgba(197, 160, 89, 0.6);
        z-index: 2;
        pointer-events: none;
    }

    /* 배너 텍스트 스타일 (그림자로 가시성 극대화) */
    .banner-text {
        position: relative;
        z-index: 3;
        color: #FDFBF7;
        font-family: 'Cinzel', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 15px rgba(0,0,0,0.5);
    }

    @keyframes subtleZoom {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }

    /* --- 🪑 컬럼(카드) 및 입력 위젯 엔틱 스타일링 --- */
    /* Streamlit 기본 컬럼을 빅토리아풍 가구처럼 변경 */
    [data-testid="column"] {
        background-color: #FDFBF7;
        padding: 25px;
        border: 3px solid #5A4222;
        border-radius: 4px;
        box-shadow: inset 0 0 0 4px #FDFBF7, inset 0 0 0 5px #C5A059, 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: inset 0 0 0 4px #FDFBF7, inset 0 0 0 5px #C5A059, 0 15px 25px rgba(0,0,0,0.2);
    }

    /* 텍스트 입력, 드롭다운, 숫자 입력창 디자인 */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stTextInput input, 
    .stNumberInput input {
        background-color: #F4EEDC !important;
        border: 1px solid #8C6D46 !important;
        color: #2C221E !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* 버튼 디자인 (엔틱 골드) */
    .stButton button {
        background-color: #4A3525 !important;
        color: #FDFBF7 !important;
        border: 1px solid #C5A059 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #634732 !important;
        border-color: #E8DCC4 !important;
        color: #FFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 명화 배너 렌더링 (가장 상단)
st.markdown("""
    <div class="artistic-banner">
        <div class="inner-gold-frame"></div>
        <h1 class="banner-text" style="font-size: 50px; margin: 0; letter-spacing: 3px;">The Cabinet of Curiosities</h1>
        <p class="banner-text" style="font-size: 20px; font-style: italic; margin-top: 15px; color: #E8DCC4; font-family: 'Playfair Display', serif;">
            Atmospheric Observations & Monetary Ledger
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. 데이터 로직 (날씨 및 환율)
load_dotenv(find_dotenv())
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city_name):
    if not WEATHER_API_KEY:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200: return res.json()
    except: pass
    return None

@st.cache_data(ttl=600)
def get_exchange_data(base_currency="USD"):
    url = f"https://api.frankfurter.app/latest?from={base_currency}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            rates = data.get("rates", {})
            rates[base_currency.upper()] = 1.0
            return rates
    except: pass
    return None

# 5. UI 레이아웃 구현
col1, col2 = st.columns(2, gap="large")

# [왼쪽] 날씨 섹션
with col1:
    st.markdown("<h2 style='font-family: Cinzel, serif; color: #3B2F2F; border-bottom: 2px solid #C5A059; padding-bottom: 10px;'>🏛️ Atmospheric Data</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; color: #7A6555; margin-bottom: 20px;'>세계 각 지역의 대기 상태를 기록합니다.</p>", unsafe_allow_html=True)
    
    city = st.text_input("도시 영문 입력", "London")
    
    if city:
        w_data = get_weather(city)
        if w_data:
            st.success(f"📍 {w_data.get('name')}, {w_data['sys'].get('country')} 관측 완료")
            c1, c2, c3 = st.columns(3)
            c1.metric("기온", f"{w_data['main']['temp']}°C")
            c2.metric("습도", f"{w_data['main']['humidity']}%")
            c3.metric("상태", w_data['weather'][0]['description'])
        else:
            st.warning("데이터를 불러올 수 없습니다.")

# [오른쪽] 환율 섹션
with col2:
    st.markdown("<h2 style='font-family: Cinzel, serif; color: #3B2F2F; border-bottom: 2px solid #C5A059; padding-bottom: 10px;'>💱 Monetary Ledger</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; color: #7A6555; margin-bottom: 20px;'>국제 통화 가치를 비교하고 환전합니다.</p>", unsafe_allow_html=True)
    
    rates_data = get_exchange_data("USD")
    if rates_data:
        curr_list = sorted(list(rates_data.keys()))
        
        ex1, ex2 = st.columns(2)
        with ex1:
            from_cur = st.selectbox("보유 자산", options=curr_list, index=curr_list.index("USD") if "USD" in curr_list else 0)
        with ex2:
            to_cur = st.selectbox("환전 자산", options=curr_list, index=curr_list.index("GBP") if "GBP" in curr_list else 1)
            
        amount = st.number_input("자본 금액 입력", min_value=0.0, value=100.0, step=10.0)
        
        custom_rates = get_exchange_data(from_cur)
        if custom_rates and to_cur in custom_rates:
            rate = custom_rates[to_cur]
            converted = amount * rate
            
            st.markdown(f"""
                <div style="background-color: #F2EBD9; padding: 15px; border-radius: 4px; border: 1px solid #C5A059; text-align: center; margin-top: 10px;">
                    <h3 style="color: #3B2F2F; margin: 0; font-family: Cinzel, serif;">{converted:,.2f} {to_cur}</h3>
                    <p style="color: #8C6D46; font-size: 13px; margin: 5px 0 0 0;">적용 환율: 1 {from_cur} = {rate:,.4f} {to_cur}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("환율 장부를 열 수 없습니다.")

# 6. 하단 챗봇 섹션
st.markdown("<br><br>", unsafe_allow_html=True)
chat_col, _ = st.columns([1, 0.01]) # 챗봇 영역도 카드 디자인을 적용하기 위해 컬럼 사용

with chat_col:
    st.markdown("<h2 style='font-family: Cinzel, serif; color: #3B2F2F; border-bottom: 2px solid #C5A059; padding-bottom: 10px;'>📜 The Scholar's Assistant</h2>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "안녕하십니까, 방문객여. 기후 상태나 통화 교환에 대해 물어보십시오. 🧐"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("질문을 남겨주십시오..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        bot_response = "그 질문에 대해서는 저도 깊은 고찰이 필요하군요. 상단의 관측 장치나 장부를 활용해 주시겠습니까?"
        if "날씨" in user_input: bot_response = "상단의 'Atmospheric Data' 영역을 활용하시면 기온을 확인하실 수 있습니다."
        elif "환율" in user_input or "환전" in user_input: bot_response = "상단의 'Monetary Ledger'에서 자본 금액을 입력하여 계산해 보십시오."

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        