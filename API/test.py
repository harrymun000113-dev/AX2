import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv, find_dotenv

# 1. 페이지 설정 (와이드 레이아웃)
st.set_page_config(
    page_title="Weather & Exchange Hub",
    page_icon="🌍",
    layout="wide"
)

# 2. 토스 스타일 트렌디한 블루 & 화이트 CSS 디자인 적용
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    .toss-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 102, 255, 0.08);
        margin-bottom: 20px;
    }
    .toss-title {
        color: #191F28;
        font-weight: 700;
        font-size: 22px;
    }
    .toss-sub {
        color: #8B95A1;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 환경변수(.env) 로드 (상위 폴더 자동 탐색)
load_dotenv(find_dotenv())
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --- 데이터 가져오기 함수들 ---

# 날씨 데이터 (OpenWeatherMap)
def get_weather(city_name):
    if not WEATHER_API_KEY:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

# 환율 데이터 (Frankfurter API - 100% 무료, 키 불필요)
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
    except:
        pass
    return None

# --- 상단 타이틀 영역 ---
st.markdown("<h1 style='color: #191F28; text-align: center; margin-bottom: 30px;'>🌤️ 글로벌 날씨 & 실시간 환율 허브</h1>", unsafe_allow_html=True)

# 3단 탭 또는 레이아웃 구성 (1단: 날씨, 2단: 환율, 3단: 챗봇)
col_weather, col_exchange = st.columns(2, gap="large")

# ==================== [영역 1] 실시간 날씨 조회 ====================
with col_weather:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="toss-title">⛅ 실시간 도시 날씨</h2>', unsafe_allow_html=True)
    st.markdown('<p class="toss-sub">원하는 도시의 날씨와 기온을 확인하세요.</p>', unsafe_allow_html=True)
    
    city = st.text_input("도시 이름 입력 (영문)", "Seoul", placeholder="예: Seoul, Tokyo, New York")
    
    if city:
        w_data = get_weather(city)
        if w_data:
            c_name = w_data.get("name")
            country = w_data["sys"].get("country")
            temp = w_data["main"]["temp"]
            feels = w_data["main"]["feels_like"]
            desc = w_data["weather"][0]["description"]
            humidity = w_data["main"]["humidity"]
            
            st.success(f"📍 **{c_name}, {country}** 날씨 정보")
            wc1, wc2, wc3 = st.columns(3)
            wc1.metric("현재 기온", f"{temp}°C", f"체감 {feels}°C")
            wc2.metric("습도", f"{humidity}%")
            wc3.metric("상태", desc)
        else:
            st.warning("도시를 찾을 수 없거나 날씨 API 키가 설정되지 않았습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== [영역 2] 실시간 환율 & 환전 계산기 ====================
with col_exchange:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="toss-title">💱 실시간 환율 및 계산기</h2>', unsafe_allow_html=True)
    st.markdown('<p class="toss-sub">세계 화폐 간의 실시간 환전 금액을 계산합니다.</p>', unsafe_allow_html=True)
    
    rates_data = get_exchange_data("USD")
    if rates_data:
        curr_list = sorted(list(rates_data.keys()))
        
        ex1, ex2 = st.columns(2)
        with ex1:
            from_cur = st.selectbox("보내는 화폐", options=curr_list, index=curr_list.index("USD") if "USD" in curr_list else 0)
        with ex2:
            to_cur = st.selectbox("받는 화폐", options=curr_list, index=curr_list.index("KRW") if "KRW" in curr_list else 1)
            
        amount = st.number_input("환전 금액", min_value=0.0, value=100.0, step=10.0)
        
        custom_rates = get_exchange_data(from_cur)
        if custom_rates and to_cur in custom_rates:
            rate = custom_rates[to_cur]
            converted = amount * rate
            
            st.markdown(f"""
                <div style="background-color: #E8F3FF; padding: 14px; border-radius: 12px; text-align: center; margin-top: 10px;">
                    <p style="color: #3182F6; font-size: 13px; margin: 0; font-weight: 600;">환전 결과</p>
                    <h3 style="color: #191F28; margin: 5px 0 0 0;">{converted:,.2f} {to_cur}</h3>
                    <p style="color: #4E5968; font-size: 11px; margin: 3px 0 0 0;">1 {from_cur} = {rate:,.4f} {to_cur}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("환율 데이터를 불러오지 못했습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== [영역 3] 트렌디한 토스 스타일 챗봇 ====================
st.markdown("---")
st.markdown('<div class="toss-card">', unsafe_allow_html=True)
st.markdown('<h2 class="toss-title">🤖 스마트 AI 어시스턴트 (챗봇)</h2>', unsafe_allow_html=True)
st.markdown('<p class="toss-sub">날씨나 환율, 여행지에 대해 무엇이든 물어보세요!</p>', unsafe_allow_html=True)

# 세션 스테이트를 이용한 채팅 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요? 날씨나 환율 정보를 편하게 물어보세요. 😊"}
    ]

# 이전 대화 내용 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if user_input := st.chat_input("메시지를 입력해주세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 챗봇 응답 로직 (간단한 키워드 매칭 및 안내 응답)
    bot_response = "죄송해요, 정확한 내용을 이해하지 못했어요. 상단의 날씨 검색이나 환율 계산기를 이용해 보시는 건 어떨까요? 💡"
    
    user_lower = user_input.lower()
    if "날씨" in user_input or "weather" in user_lower:
        bot_response = "날씨가 궁금하시군요! 상단의 **'실시간 도시 날씨'** 카드에서 원하시는 도시 영문 이름을 입력하시면 실시간 기온과 상태를 바로 확인하실 수 있습니다."
    elif "환율" in user_input or "환전" in user_input or "exchange" in user_lower:
        bot_response = "환율 계산이 필요하시군요! 상단의 **'실시간 환율 및 계산기'**에서 보내고 받는 화폐를 선택하고 금액을 넣으시면 자동으로 계산됩니다."
    elif "안녕" in user_input or "hello" in user_lower:
        bot_response = "반갑습니다! 오늘 날씨와 환율 확인에 유용한 하루가 되시길 바랍니다. 추가로 궁금한 점이 있으신가요?"

    # 챗봇 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

st.markdown('</div>', unsafe_allow_html=True)