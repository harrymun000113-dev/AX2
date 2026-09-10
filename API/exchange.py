import requests
import streamlit as st
import pandas as pd

# 1. 페이지 설정 (토스 스타일 대시보드 & 와이드 레이아웃)
st.set_page_config(
    page_title="Toss Exchange",
    page_icon="💸",
    layout="wide"
)

# 2. 토스 스타일 디자인 CSS 적용 (직관적이고 친근한 블루 & 화이트 톤)
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
        font-size: 24px;
    }
    .toss-sub {
        color: #8B95A1;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Frankfurter API 데이터 호출 함수 (키 불필요, 100% 무료 및 안정적)
@st.cache_data(ttl=600) # 10분 캐싱
def get_exchange_data(base_currency="USD"):
    url = f"https://api.frankfurter.app/latest?from={base_currency}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            # 기준 통화 자신도 1.0으로 추가
            rates[base_currency.upper()] = 1.0
            return rates
        else:
            return None
    except Exception as e:
        return None

# 데이터 로드 (미국 달러 기준)
rates_data = get_exchange_data("USD")

if not rates_data:
    st.error("🚨 환율 데이터를 불러오는 중 네트워크 오류가 발생했습니다.")
    st.stop()

currency_list = sorted(list(rates_data.keys()))

# --- UI 레이아웃 구성 (2단 컬럼: 왼쪽 주요 환율 / 오른쪽 환전 계산기) ---
col_left, col_right = st.columns([1.1, 1.4], gap="large")

# [왼쪽 영역] 주요 10개국 실시간 환율 정보
with col_left:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown("### 📊 주요 10개국 실시간 환율")
    st.markdown('<p class="toss-sub">미국 달러(USD) 기준 주요 통화 흐름</p>', unsafe_allow_html=True)
    
    # 대표적인 주요 10개 통화 (데이터에 존재하는 것만 필터링)
    target_major = ["KRW", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD"]
    major_currencies = [cur for cur in target_major if cur in rates_data]
    
    major_data = []
    for cur in major_currencies:
        val = rates_data[cur]
        major_data.append({
            "통화 코드": cur, 
            "환율 (USD 1달러 기준)": f"{val:,.2f}"
        })
            
    if major_data:
        df_major = pd.DataFrame(major_data)
        st.dataframe(df_major, use_container_width=True, hide_index=True)
    else:
        st.warning("표시할 주요 통화 데이터가 없습니다.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# [오른쪽 영역] 실시간 환전 계산기
with col_right:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="toss-title">💱 실시간 환전 계산기</h2>', unsafe_allow_html=True)
    st.markdown('<p class="toss-sub">원하는 화폐를 선택하고 금액을 입력하면 자동으로 계산됩니다.</p>', unsafe_allow_html=True)
    
    # 드롭다운 기본 인덱스 설정 안전장치
    default_from_idx = currency_list.index("USD") if "USD" in currency_list else 0
    default_to_idx = currency_list.index("KRW") if "KRW" in currency_list else (1 if len(currency_list) > 1 else 0)

    c1, c2 = st.columns(2)
    with c1:
        from_currency = st.selectbox("보내는 화폐", options=currency_list, index=default_from_idx)
    with c2:
        to_currency = st.selectbox("받는 화폐", options=currency_list, index=default_to_idx)
        
    # 금액 입력창
    amount = st.number_input("환전할 금액", min_value=0.0, value=100.0, step=10.0)
    
    # 선택한 '보내는 화폐' 기준으로 상대 환율 재계산
    custom_rates = get_exchange_data(from_currency)
    
    if custom_rates and to_currency in custom_rates:
        rate = custom_rates[to_currency]
        converted = amount * rate
        
        st.markdown("<br>", unsafe_allow_html=True)
        # 토스 시그니처 블루 컬러 톤의 결과 카드
        st.markdown(f"""
            <div style="background-color: #E8F3FF; padding: 22px; border-radius: 16px; text-align: center;">
                <p style="color: #3182F6; font-size: 14px; margin-bottom: 5px; font-weight: 600;">환전 결과</p>
                <h1 style="color: #191F28; font-size: 32px; margin: 0;">{converted:,.2f} <span style="font-size: 20px;">{to_currency}</span></h1>
                <p style="color: #4E5968; font-size: 13px; margin-top: 8px;">적용 환율: 1 {from_currency} = {rate:,.4f} {to_currency}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("환율 데이터를 계산할 수 없습니다.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    # af