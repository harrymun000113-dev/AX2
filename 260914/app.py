import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
from dotenv import load_dotenv

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="Korean Air Style Travel Helper", page_icon="✈️", layout="wide")

# --- 대한항공 스타일 CSS ---
st.markdown("""
<style>
    /* 전체 폰트 및 배경 (대한항공 특유의 실버/화이트 배경) */
    .stApp { background-color: #F4F5F8; font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; }
    
    /* 사이드바 */
    div[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E1EDFA; }
    
    /* 카드 디자인 (여행지 핀셋) */
    .place-card { background-color: #FFFFFF; border-radius: 8px; padding: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 12px; border-left: 5px solid #0064DE; }
    .place-title { font-size: 15px; font-weight: 700; color: #111111; margin-bottom: 4px; }
    .place-addr { font-size: 12px; color: #666666; margin-bottom: 8px; }
    
    /* 버튼 스타일 (대한항공 시그니처 블루) */
    .stButton > button { border-radius: 6px; font-weight: 600; transition: all 0.2s; border: 1px solid #E1EDFA; }
    button[kind="primary"] { background-color: #0064DE !important; color: white !important; border: none !important; }
    button[kind="primary"]:hover { background-color: #004CB3 !important; }
    
    /* 상단 대시보드 패널 */
    .top-panel { background-color: #FFFFFF; border: 1px solid #E1EDFA; border-radius: 10px; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
    .rate-box { display: flex; gap: 40px; }
    .info-item { text-align: center; }
    .info-title { font-size: 12px; color: #888888; font-weight: 600; margin-bottom: 5px; }
    .info-value { font-size: 18px; font-weight: 800; color: #0064DE; }
    .weather-box { border-left: 1px solid #E1EDFA; padding-left: 40px; display: flex; align-items: center; gap: 10px; }
    
    /* 축제 카드 */
    .festival-box { background-color: #FFFFFF; border: 1px solid #E1EDFA; border-radius: 8px; padding: 15px; text-align: center; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
</style>
""", unsafe_allow_html=True)

# --- 환경변수 로드 ---
load_dotenv()
def get_secret(key_name):
    if key_name in st.secrets: return st.secrets[key_name]
    return os.getenv(key_name, "")

KAKAO_JS_KEY = get_secret("KAKAO_JS_KEY")
KAKAO_REST_KEY = get_secret("KAKAO_REST_KEY")
OPENWEATHER_KEY = get_secret("OPENWEATHER_API_KEY")

# --- 상태 초기화 ---
if "saved_places" not in st.session_state: st.session_state.saved_places = []
if "search_results" not in st.session_state: st.session_state.search_results = []

# --- API 연동 함수 (캐싱 적용으로 속도 최적화) ---
@st.cache_data(ttl=3600)
def fetch_exchange_rates():
    try:
        res = requests.get("https://open.er-api.com/v6/latest/KRW", timeout=5).json()
        r = res.get('rates', {})
        if r: return { "USD": f"{1/r.get('USD', 1):.2f}", "EUR": f"{1/r.get('EUR', 1):.2f}", "JPY": f"{100/r.get('JPY', 1):.2f}", "CNY": f"{1/r.get('CNY', 1):.2f}", "GBP": f"{1/r.get('GBP', 1):.2f}" }
    except: pass
    return {k: "-" for k in ["USD", "EUR", "JPY", "CNY", "GBP"]}

@st.cache_data(ttl=1800)
def fetch_weather(api_key):
    if not api_key: return None
    try:
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Seoul,KR&appid={api_key}&units=metric&lang=kr", timeout=5).json()
        if res.get("cod") == 200:
            return {"temp": f"{res['main']['temp']:.1f}", "desc": res['weather'][0]['description'], "icon": f"http://openweathermap.org/img/wn/{res['weather'][0]['icon']}.png"}
    except: pass
    return None

def search_kakao_places(keyword):
    try:
        res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers={"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}, params={"query": keyword, "size": 5})
        if res.status_code == 200: return res.json().get("documents", [])
    except: pass
    return []

# --- 데이터: 프리셋 및 9월 축제 ---
PRESETS = {
    "☕ 유명 카페": [
        {"id": "p1", "place_name": "어니언 안국", "address_name": "서울 종로구 계동길 5", "road_address_name": "계동길 5", "x": "126.986", "y": "37.576"},
        {"id": "p2", "place_name": "테라로사 커피공장", "address_name": "강원 강릉시 구정면 현천길 25", "road_address_name": "", "x": "128.877", "y": "37.696"},
        {"id": "p3", "place_name": "몽상드애월", "address_name": "제주 제주시 애월읍 애월북서길 56-1", "road_address_name": "", "x": "126.308", "y": "33.462"},
        {"id": "p4", "place_name": "웨이브온 커피", "address_name": "부산 기장군 장안읍 해맞이로 286", "road_address_name": "", "x": "129.273", "y": "35.319"},
        {"id": "p5", "place_name": "카멜커피 성수", "address_name": "서울 성동구 성수이로14길 14", "road_address_name": "", "x": "127.056", "y": "37.544"}
    ],
    "🏛️ 역사적인 장소": [
        {"id": "p6", "place_name": "경복궁", "address_name": "서울 종로구 사직로 161", "road_address_name": "", "x": "126.977", "y": "37.579"},
        {"id": "p7", "place_name": "불국사", "address_name": "경북 경주시 불국로 385", "road_address_name": "", "x": "129.332", "y": "35.790"},
        {"id": "p8", "place_name": "수원 화성", "address_name": "경기 수원시 장안구 영화동 320-2", "road_address_name": "", "x": "127.011", "y": "37.287"},
        {"id": "p9", "place_name": "창덕궁", "address_name": "서울 종로구 율곡로 99", "road_address_name": "", "x": "126.991", "y": "37.579"},
        {"id": "p10", "place_name": "하회마을", "address_name": "경북 안동시 풍천면 하회종가길 2-1", "road_address_name": "", "x": "128.517", "y": "36.538"}
    ],
    "🍲 유명 맛집": [
        {"id": "p11", "place_name": "명동교자 본점", "address_name": "서울 중구 명동10길 29", "road_address_name": "", "x": "126.985", "y": "37.562"},
        {"id": "p12", "place_name": "해운대 암소갈비집", "address_name": "부산 해운대구 중동2로10번길 32-10", "road_address_name": "", "x": "129.166", "y": "35.163"},
        {"id": "p13", "place_name": "성심당 본점", "address_name": "대전 중구 대종로480번길 15", "road_address_name": "", "x": "127.427", "y": "36.327"},
        {"id": "p14", "place_name": "우래옥", "address_name": "서울 중구 창경궁로 62-29", "road_address_name": "", "x": "126.998", "y": "37.568"},
        {"id": "p15", "place_name": "자매국수", "address_name": "제주 제주시 탑동로 11", "road_address_name": "", "x": "126.525", "y": "33.516"}
    ],
    "🗼 필수 여행지": [
        {"id": "p16", "place_name": "N서울타워", "address_name": "서울 용산구 남산공원길 105", "road_address_name": "", "x": "126.988", "y": "37.551"},
        {"id": "p17", "place_name": "해운대 해수욕장", "address_name": "부산 해운대구 우동", "road_address_name": "", "x": "129.160", "y": "35.158"},
        {"id": "p18", "place_name": "전주 한옥마을", "address_name": "전북 전주시 완산구 기린대로 99", "road_address_name": "", "x": "127.152", "y": "35.815"},
        {"id": "p19", "place_name": "성산일출봉", "address_name": "제주 서귀포시 성산읍 성산리 1", "road_address_name": "", "x": "126.942", "y": "33.458"},
        {"id": "p20", "place_name": "남이섬", "address_name": "강원 춘천시 남산면 남이섬길 1", "road_address_name": "", "x": "127.525", "y": "37.791"}
    ]
}

FESTIVALS = [
    {"id": "f1", "place_name": "평창효석문화제", "address_name": "강원 평창군 봉평면 이효석길 157", "road_address_name": "이효석길 157", "x": "128.379", "y": "37.616", "desc": "9.4 ~ 9.13"},
    {"id": "f2", "place_name": "무주반딧불축제", "address_name": "전북 무주군 무주읍 한풍루로 326-17", "road_address_name": "한풍루로 326-17", "x": "127.662", "y": "36.009", "desc": "9.4 ~ 9.12"},
    {"id": "f3", "place_name": "덕수궁 밤의 석조전", "address_name": "서울 중구 세종대로 99", "road_address_name": "세종대로 99", "x": "126.974", "y": "37.565", "desc": "9.9 ~ 10.18"},
    {"id": "f4", "place_name": "춘천인형극제", "address_name": "강원 춘천시 영서로 3017", "road_address_name": "영서로 3017", "x": "127.729", "y": "37.881", "desc": "9.10 ~ 9.16"},
    {"id": "f5", "place_name": "서울국제작가축제", "address_name": "서울 종로구 인사동9길 26", "road_address_name": "인사동9길 26", "x": "126.983", "y": "37.574", "desc": "9.11 ~ 9.16"},
]

def add_preset(category):
    saved_ids = [p['id'] for p in st.session_state.saved_places]
    for p in PRESETS[category]:
        if p['id'] not in saved_ids:
            st.session_state.saved_places.append(p)

# ==========================================
# 1. 사이드바 (핀셋 및 프리셋)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#0064DE;'>✈️ KOREA TRAVEL</h2>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🧳 테마별 코스 담기")
    st.caption("조나 히마리 같은 외국인 친구를 가이드할 때도 유용한 필수 코스입니다.")
    col1, col2 = st.columns(2)
    if col1.button("☕ 유명 카페", use_container_width=True): add_preset("☕ 유명 카페")
    if col2.button("🏛️ 역사적인 장소", use_container_width=True): add_preset("🏛️ 역사적인 장소")
    if col1.button("🍲 유명 맛집", use_container_width=True): add_preset("🍲 유명 맛집")
    if col2.button("🗼 필수 여행지", use_container_width=True): add_preset("🗼 필수 여행지")
    
    st.divider()
    st.markdown("### 📌 여행지 핀셋")
    if not st.session_state.saved_places:
        st.info("우측 검색창이나 프리셋을 이용해 여행지를 담아보세요!")
    else:
        for idx, place in enumerate(st.session_state.saved_places):
            st.markdown(f"""
            <div class="place-card">
                <div class="place-title">{place['place_name']}</div>
                <div class="place-addr">{place['address_name']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("삭제", key=f"del_{place['id']}_{idx}", use_container_width=True):
                st.session_state.saved_places.pop(idx)
                st.rerun()

# ==========================================
# 2. 메인 대시보드 (환율, 날씨)
# ==========================================
rates = fetch_exchange_rates()
weather = fetch_weather(OPENWEATHER_KEY)
weather_html = f"<img src='{weather['icon']}' width='30' style='vertical-align:middle;'> {weather['temp']}°C, {weather['desc']}" if weather else "데이터 없음"

st.markdown(f"""
<div class="top-panel">
    <div class="rate-box">
        <div class="info-item"><div class="info-title">USD/KRW</div><div class="info-value">{rates['USD']}</div></div>
        <div class="info-item"><div class="info-title">EUR/KRW</div><div class="info-value">{rates['EUR']}</div></div>
        <div class="info-item"><div class="info-title">JPY(100)/KRW</div><div class="info-value">{rates['JPY']}</div></div>
        <div class="info-item"><div class="info-title">CNY/KRW</div><div class="info-value">{rates['CNY']}</div></div>
        <div class="info-item"><div class="info-title">GBP/KRW</div><div class="info-value">{rates['GBP']}</div></div>
    </div>
    <div class="weather-box">
        <div class="info-item"><div class="info-title">SEOUL WEATHER</div><div class="info-value" style="color:#111; font-size:16px;">{weather_html}</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. 지도 및 검색 레이아웃
# ==========================================
col_map, col_search = st.columns([7, 3], gap="large")

with col_map:
    markers_data = []
    for p in st.session_state.saved_places:
        markers_data.append({"name": f"💖 [저장됨] {p['place_name']}", "lat": float(p['y']), "lng": float(p['x'])})
        
    saved_ids = [p['id'] for p in st.session_state.saved_places]
    for p in st.session_state.search_results:
        if p['id'] not in saved_ids:
            markers_data.append({"name": p['place_name'], "lat": float(p['y']), "lng": float(p['x'])})
            
    markers_json = json.dumps(markers_data, ensure_ascii=False)

    if not KAKAO_JS_KEY:
        st.error("🚨 카카오 JavaScript API 키가 설정되지 않았습니다.")
    else:
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
            <meta name="referrer" content="unsafe-url">
            <style>
                html, body {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
                #map {{ width: 100%; height: 600px; border: 1px solid #E1EDFA; border-radius: 12px; overflow: hidden; box-sizing: border-box; background-color: #f8f9fa; }}
                .info-window {{ padding: 8px; font-size: 14px; font-family: 'Malgun Gothic', sans-serif; font-weight: bold; border-radius:8px; border:none; color:#0064DE; }}
            </style>
            <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false"></script>
        </head>
        <body>
            <div id="map"></div>
            <script>
                window.onload = function() {{
                    if (typeof kakao === 'undefined') return;
                    kakao.maps.load(function() {{
                        var mapContainer = document.getElementById('map'); 
                        var mapOption = {{ center: new kakao.maps.LatLng(37.5665, 126.9780), level: 8 }};
                        var map = new kakao.maps.Map(mapContainer, mapOption);
                        var zoomControl = new kakao.maps.ZoomControl();
                        map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

                        var markers = {markers_json};
                        var bounds = new kakao.maps.LatLngBounds();
                        var hasMarkers = false;
                        
                        markers.forEach(function(item) {{
                            var markerPos = new kakao.maps.LatLng(item.lat, item.lng); 
                            var marker = new kakao.maps.Marker({{ position: markerPos }});
                            marker.setMap(map);
                            bounds.extend(markerPos);
                            hasMarkers = true;
                            
                            var infowindow = new kakao.maps.InfoWindow({{ content: '<div class="info-window">' + item.name + '</div>' }});
                            kakao.maps.event.addListener(marker, 'mouseover', function() {{ infowindow.open(map, marker); }});
                            kakao.maps.event.addListener(marker, 'mouseout', function() {{ infowindow.close(); }});
                        }});
                        
                        if (hasMarkers) map.setBounds(bounds);
                    }});
                }};
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=620)

with col_search:
    st.markdown("<h3 style='color:#0064DE;'>🔍 장소 검색</h3>", unsafe_allow_html=True)
    search_keyword = st.text_input("검색어 입력", placeholder="예: 해운대 맛집", label_visibility="collapsed")
    
    if st.button("검색하기", use_container_width=True, type="primary"):
        if not KAKAO_REST_KEY: st.error("REST API 키가 없어 검색할 수 없습니다.")
        elif search_keyword:
            with st.spinner("검색 중..."):
                st.session_state.search_results = search_kakao_places(search_keyword)
    
    st.divider()
    if st.session_state.search_results:
        st.markdown(f"**총 {len(st.session_state.search_results)}개의 결과**")
        for res in st.session_state.search_results:
            with st.container():
                st.markdown(f"**{res['place_name']}**")
                st.caption(f"{res['road_address_name'] or res['address_name']}")
                
                if any(p['id'] == res['id'] for p in st.session_state.saved_places):
                    st.button("✅ 이미 저장됨", key=f"saved_{res['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("📍 핀셋에 담기", key=f"save_{res['id']}", use_container_width=True):
                        st.session_state.saved_places.append(res)
                        st.rerun()
                st.markdown("---")

# ==========================================
# 4. 하단 9월 대표 축제
# ==========================================
st.markdown("<h3 style='color:#0064DE; margin-top:30px;'>🎊 2026년 9월 대표 축제</h3>", unsafe_allow_html=True)
festival_cols = st.columns(5)

for i, fes in enumerate(FESTIVALS):
    with festival_cols[i]:
        st.markdown(f"""
        <div class="festival-box">
            <h4 style="margin:0; font-size:16px; color:#111;">{fes['place_name']}</h4>
            <p style="margin:5px 0 10px 0; font-size:13px; color:#666;">{fes['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("지도에서 위치 보기", key=f"fes_btn_{i}", use_container_width=True):
            st.session_state.search_results = [fes]
            st.rerun()