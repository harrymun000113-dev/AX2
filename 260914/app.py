import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
from dotenv import load_dotenv

st.set_page_config(page_title="한국 여행 헬퍼", page_icon="🧳", layout="wide")

st.markdown("""
<style>
    .block-container { max-width: 1400px; padding-top: 2rem; }
    div[data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E9ECEF; }
    .place-card { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #F1F3F5; }
    .place-title { font-size: 16px; font-weight: bold; color: #343A40; margin-bottom: 5px; }
    .place-addr { font-size: 12px; color: #868E96; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

load_dotenv()

def get_secret(key_name):
    if key_name in st.secrets:
        return st.secrets[key_name]
    return os.getenv(key_name, "")

KAKAO_JS_KEY = get_secret("KAKAO_JS_KEY")
KAKAO_REST_KEY = get_secret("KAKAO_REST_KEY")
OPENWEATHER_KEY = get_secret("OPENWEATHER_API_KEY")

if "saved_places" not in st.session_state:
    st.session_state.saved_places = []
if "search_results" not in st.session_state:
    st.session_state.search_results = []

def search_kakao_places(keyword):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    params = {"query": keyword, "size": 5}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("documents", [])
    except Exception as e:
        st.error(f"검색 중 오류 발생: {e}")
    return []

with st.sidebar:
    st.title("🧳 한국 여행 헬퍼")
    
    st.markdown("### 🔌 API 상태 체커")
    st.caption(f"{'✅' if KAKAO_JS_KEY else '❌'} 카카오 맵 API (JS)")
    st.caption(f"{'✅' if KAKAO_REST_KEY else '❌'} 카카오 검색 API (REST)")
    st.caption(f"{'✅' if OPENWEATHER_KEY else '❌'} OpenWeather API")
    st.divider()
    
    st.markdown("### 📌 여행지 핀셋")
    if not st.session_state.saved_places:
        st.info("우측 검색창을 이용해 여행지를 담아보세요!")
    else:
        for idx, place in enumerate(st.session_state.saved_places):
            st.markdown(f"""
            <div class="place-card">
                <div class="place-title">📍 {place['place_name']}</div>
                <div class="place-addr">{place['address_name']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("삭제", key=f"del_{place['id']}_{idx}", use_container_width=True):
                st.session_state.saved_places.pop(idx)
                st.rerun()

col_map, col_search = st.columns([7, 3], gap="large")

with col_map:
    st.markdown("### 🗺️ 지도 뷰")
    
    markers_data = []
    
    for p in st.session_state.saved_places:
        markers_data.append({
            "name": f"💖 [저장됨] {p['place_name']}",
            "lat": float(p['y']), "lng": float(p['x'])
        })
        
    saved_ids = [p['id'] for p in st.session_state.saved_places]
    for p in st.session_state.search_results:
        if p['id'] not in saved_ids:
            markers_data.append({
                "name": p['place_name'],
                "lat": float(p['y']), "lng": float(p['x'])
            })
            
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
                #map {{ width: 100%; height: 600px; border: 1px solid #E9ECEF; border-radius: 12px; overflow: hidden; box-sizing: border-box; background-color: #f8f9fa; }}
                .info-window {{ padding: 8px; font-size: 14px; font-family: 'Malgun Gothic', sans-serif; font-weight: bold; border-radius:8px; border:none; }}
            </style>
            <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false"></script>
        </head>
        <body>
            <div id="map"></div>
            <script>
                window.onload = function() {{
                    if (typeof kakao === 'undefined') {{
                        document.getElementById('map').innerHTML = 
                            "<div style='padding:20px; text-align:center; color:red; margin-top:50px;'>" +
                            "<h3>🚨 카카오맵 로드 차단됨</h3>" +
                            "<p>API 키 또는 카카오 도메인 설정을 다시 확인해주세요.</p></div>";
                        return;
                    }}
                    
                    kakao.maps.load(function() {{
                        var mapContainer = document.getElementById('map'); 
                        var mapOption = {{
                            center: new kakao.maps.LatLng(37.5665, 126.9780), 
                            level: 7
                        }};

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
                            
                            var infowindow = new kakao.maps.InfoWindow({{
                                content: '<div class="info-window">' + item.name + '</div>'
                            }});
                            
                            kakao.maps.event.addListener(marker, 'mouseover', function() {{ infowindow.open(map, marker); }});
                            kakao.maps.event.addListener(marker, 'mouseout', function() {{ infowindow.close(); }});
                        }});
                        
                        if (hasMarkers) {{
                            map.setBounds(bounds);
                        }}
                    }});
                }};
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=620)

with col_search:
    st.markdown("### 🔍 장소 검색")
    search_keyword = st.text_input("검색어 입력", placeholder="예: 해운대 맛집", label_visibility="collapsed")
    
    if st.button("검색하기", use_container_width=True, type="primary"):
        if not KAKAO_REST_KEY:
            st.error("REST API 키가 없어 검색할 수 없습니다.")
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
                
                is_saved = any(p['id'] == res['id'] for p in st.session_state.saved_places)
                
                if is_saved:
                    st.button("✅ 이미 저장됨", key=f"saved_{res['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("📍 핀셋에 담기", key=f"save_{res['id']}", use_container_width=True):
                        st.session_state.saved_places.append(res)
                        st.rerun()
                st.markdown("---")