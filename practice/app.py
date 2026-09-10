import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="Build Your Osaka", initial_sidebar_state="collapsed")

# 2. 로컬 사진 파일을 HTML에 넣을 수 있도록 Base64로 변환하는 함수
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    else:
        return ""

# 폴더에 저장된 사진 이름 지정 (app.py와 동일한 폴더에 있어야 합니다)
img_dotonbori = get_base64_image("dotonbori.jpg")
img_osaka = get_base64_image("osaka.jpg")

# 3. 글로벌 CSS: 몽환적인 파스텔 구름 배경 고정
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1300px; }
    
    .stApp {
        background-color: #a1c4fd;
        background-image: url('https://images.unsplash.com/photo-1509803874385-db7c23652552?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

# 4. 레이아웃 분할 (좌측 1 : 중앙 1.8 : 우측 1 비율)
col_left, col_mid, col_right = st.columns([1, 1.8, 1])

# ==========================================
# 🌤️ [좌측] 실시간 글로벌 날씨 위젯
# ==========================================
with col_left:
    weather_widget_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
        body { margin: 0; padding: 10px; font-family: 'Pretendard', sans-serif; }
        .glass-card {
            background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 24px; padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15), inset 0 0 0 1px rgba(255,255,255,0.2);
            color: #1e293b;
        }
        h3 { margin-top: 0; font-size: 18px; display: flex; align-items: center; gap: 8px;}
        select {
            width: 100%; padding: 12px; border-radius: 14px; background: rgba(255, 255, 255, 0.4); 
            border: 1px solid rgba(255,255,255,0.6); font-size: 14px; color: #1e293b; margin-bottom: 20px; outline: none;
        }
        .weather-info { text-align: center; margin-top: 20px; }
        .temp { font-size: 52px; font-weight: 700; margin: 10px 0; letter-spacing: -2px; }
        .desc { font-size: 16px; font-weight: 600; color: #334155;}
        .details { display: flex; justify-content: space-between; margin-top: 30px; padding-top: 20px; border-top: 1px dashed rgba(255,255,255,0.5); }
        .detail-item { text-align: center; font-size: 13px; color: #475569;}
        .detail-item span { display: block; font-weight: 700; font-size: 16px; color: #1e293b; margin-top: 4px;}
    </style>
    </head>
    <body>
        <div class="glass-card">
            <h3>☁️ Global Weather</h3>
            <select id="citySelect" onchange="fetchWeather()">
                <option value="34.69,135.50">Osaka, Japan</option>
                <option value="37.56,126.97">Seoul, South Korea</option>
                <option value="35.68,139.69">Tokyo, Japan</option>
            </select>
            <div class="weather-info"><div class="desc" id="w-desc">Loading...</div><div class="temp" id="w-temp">--°C</div></div>
            <div class="details">
                <div class="detail-item">Wind<span id="w-wind">-- km/h</span></div>
                <div class="detail-item">Humidity<span id="w-hum">-- %</span></div>
            </div>
        </div>
        <script>
            async function fetchWeather() {
                const coords = document.getElementById('citySelect').value.split(',');
                const url = `https://api.open-meteo.com/v1/forecast?latitude=${coords[0]}&longitude=${coords[1]}&current_weather=true&hourly=relativehumidity_2m`;
                try {
                    const res = await fetch(url); const data = await res.json();
                    document.getElementById('w-temp').innerText = Math.round(data.current_weather.temperature) + '°C';
                    document.getElementById('w-wind').innerText = data.current_weather.windspeed + ' km/h';
                    document.getElementById('w-hum').innerText = data.hourly.relativehumidity_2m[0] + '%';
                    document.getElementById('w-desc').innerText = data.current_weather.weathercode < 4 ? "Clear/Cloudy" : "Rain/Snow";
                } catch(e) {}
            }
            fetchWeather();
        </script>
    </body>
    </html>
    """
    components.html(weather_widget_html, height=450)


# ==========================================
# 💱 [중앙] 계산기 & 로컬 이미지 기반 여행 정보
# ==========================================
with col_mid:
    # 1) 투명 버튼 글래스모피즘 계산기 (바디 여백과 높이를 넉넉히 늘림)
    calc_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
        /* 그림자가 잘리지 않도록 body에 padding을 20px로 넉넉하게 주었습니다 */
        body { margin: 0; padding: 20px; font-family: 'Pretendard', sans-serif; display: flex; justify-content: center; }
        .calc-glass {
            background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 32px; width: 100%; max-width: 500px; padding: 35px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        }
        .display-area { text-align: right; margin-bottom: 25px; }
        .currency-label { font-size: 14px; color: #334155; margin-bottom: 5px; font-weight: 700; }
        .number-display { font-size: 52px; font-weight: 700; color: #0f172a; word-break: break-all; letter-spacing: -1px;}
        .keypad { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .btn {
            background: rgba(255, 255, 255, 0.3); border: 1px solid rgba(255, 255, 255, 0.6); 
            border-radius: 20px; aspect-ratio: 1.1; font-size: 24px; font-weight: 600; color: #1e293b; cursor: pointer;
        }
        .btn:active { background: rgba(255, 255, 255, 0.5); transform: scale(0.95); }
        .btn-action { background: rgba(255, 255, 255, 0.6); color: #0f172a; }
        .btn-convert { background: rgba(255, 255, 255, 0.9); color: #0284c7; font-size: 26px; }
    </style>
    </head>
    <body>
        <div class="calc-glass">
            <div class="display-area">
                <div class="currency-label" id="mode-label">KRW ⇄ JPY Exchange</div>
                <div class="number-display" id="display">0</div>
            </div>
            <div class="keypad">
                <button class="btn" onclick="input('7')">7</button><button class="btn" onclick="input('8')">8</button>
                <button class="btn" onclick="input('9')">9</button><button class="btn btn-action" onclick="clearDisp()">C</button>
                <button class="btn" onclick="input('4')">4</button><button class="btn" onclick="input('5')">5</button>
                <button class="btn" onclick="input('6')">6</button><button class="btn btn-action" onclick="del()">←</button>
                <button class="btn" onclick="input('1')">1</button><button class="btn" onclick="input('2')">2</button>
                <button class="btn" onclick="input('3')">3</button><button class="btn btn-convert" onclick="calc('JPY')">¥</button>
                <button class="btn" onclick="input('00')">00</button><button class="btn" onclick="input('0')">0</button>
                <button class="btn" onclick="input('.')">.</button><button class="btn btn-convert" onclick="calc('KRW')">₩</button>
            </div>
        </div>
        <script>
            let current = '0'; const rate = 9.1; const display = document.getElementById('display');
            function update() { display.innerText = current.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ","); }
            function input(v) { current = (current === '0' && v !== '.') ? v : current + v; update(); }
            function clearDisp() { current = '0'; document.getElementById('mode-label').innerText = "INPUT AMOUNT"; update(); }
            function del() { current = current.slice(0, -1); if(current === '') current = '0'; update(); }
            function calc(curr) {
                let num = parseFloat(current.replace(/,/g, '')); if(isNaN(num)) return;
                if(curr === 'JPY') { current = "¥ " + Math.floor(num / rate).toLocaleString(); document.getElementById('mode-label').innerText = "Result (KRW → JPY)"; }
                else { current = "₩ " + Math.floor(num * rate).toLocaleString(); document.getElementById('mode-label').innerText = "Result (JPY → KRW)"; }
                display.innerText = current; current = '0';
            }
        </script>
    </body>
    </html>
    """
    # 💡 잘림 현상을 완벽히 방지하기 위해 높이를 620으로 매우 넉넉하게 늘렸습니다.
    components.html(calc_html, height=620)

    # 2) 노트북 로컬 사진 렌더링
    st.markdown(f"""
    <style>
        .travel-native-glass {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 24px;
            padding: 25px;
            margin: 10px auto 25px auto;
            max-width: 500px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            display: flex;
            align-items: center;
            gap: 20px;
            font-family: 'Pretendard', sans-serif;
            color: #1e293b;
        }}
        .travel-native-glass img {{
            width: 140px; height: 140px; object-fit: cover; border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background-color: #f1f5f9;
        }}
        .travel-info-h3 {{ margin: 0 0 8px 0; color: #1e293b; font-size: 20px; font-weight: 700; }}
        .travel-info-p {{ margin: 0; color: #334155; line-height: 1.5; font-size: 14px; }}
    </style>

    <div class="travel-native-glass">
        <img src="data:image/jpeg;base64,{img_dotonbori}" alt="Dotonbori">
        <div>
            <div class="travel-info-h3">Dotonbori District</div>
            <div class="travel-info-p">오사카의 밤을 밝히는 네온사인의 거리. 글리코상 앞에서 사진을 찍고 최고의 길거리 음식을 즐겨보세요.</div>
        </div>
    </div>

    <div class="travel-native-glass">
        <img src="data:image/jpeg;base64,{img_osaka}" alt="Osaka Castle">
        <div>
            <div class="travel-info-h3">Osaka Castle</div>
            <div class="travel-info-p">웅장한 석벽과 화려한 텐슈카쿠가 돋보이는 오사카의 랜드마크. 일본의 정취를 깊게 느껴보세요.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 📈 [우측] 실시간 Top 10 통화 환율 위젯
# ==========================================
with col_right:
    currency_widget_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
        body { margin: 0; padding: 10px; font-family: 'Pretendard', sans-serif; }
        .glass-card {
            background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 24px; padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15); height: 100%; color: #1e293b;
        }
        h3 { margin-top: 0; font-size: 18px; margin-bottom: 20px;}
        .curr-row {
            display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.4);
        }
        .curr-row:last-child { border: none; }
        .flag-code { display: flex; align-items: center; gap: 10px; font-weight: 600; }
        .rate { font-weight: 700; color: #0f172a; }
        .base-label { font-size: 12px; color: #475569; text-align: right; margin-bottom: 10px; }
    </style>
    </head>
    <body>
        <div class="glass-card">
            <h3>📈 Top 10 Exchange Rates</h3>
            <div class="base-label">Base: 1 Foreign Currency = ? KRW</div>
            <div id="rates-container"><div style="text-align:center;">Loading...</div></div>
        </div>
        <script>
            const currencies = [
                {code: 'USD', flag: '🇺🇸'}, {code: 'JPY', flag: '🇯🇵'}, {code: 'EUR', flag: '🇪🇺'},
                {code: 'GBP', flag: '🇬🇧'}, {code: 'AUD', flag: '🇦🇺'}, {code: 'CAD', flag: '🇨🇦'},
                {code: 'CHF', flag: '🇨🇭'}, {code: 'CNY', flag: '🇨🇳'}, {code: 'HKD', flag: '🇭🇰'},
                {code: 'SGD', flag: '🇸🇬'}
            ];
            async function fetchRates() {
                try {
                    const res = await fetch('https://api.exchangerate-api.com/v4/latest/KRW'); const data = await res.json();
                    let html = '';
                    currencies.forEach(c => {
                        let rateToKrw = 1 / data.rates[c.code]; if (c.code === 'JPY') rateToKrw = rateToKrw * 100;
                        html += `<div class="curr-row"><div class="flag-code"><span>${c.flag}</span> ${c.code === 'JPY' ? 'JPY (100)' : c.code}</div><div class="rate">₩ ${rateToKrw.toFixed(2)}</div></div>`;
                    });
                    document.getElementById('rates-container').innerHTML = html;
                } catch(e) {}
            }
            fetchRates();
        </script>
    </body>
    </html>
    """
    components.html(currency_widget_html, height=620)

# ==========================================
# ✈️ 하단 고정 글래스모피즘 CTA 예약 버튼
# ==========================================
st.markdown("""
<div style="text-align: center; margin: 40px 0;">
    <a href="https://www.skyscanner.co.kr/transport/flights/sela/edi/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&oym=2610&iym=2610&selectedoday=01&selectediday=01" target="_blank" 
       style="display: inline-block; 
              background: rgba(255, 255, 255, 0.4); 
              backdrop-filter: blur(12px); 
              -webkit-backdrop-filter: blur(12px);
              border: 2px solid rgba(255, 255, 255, 0.8); 
              border-radius: 50px; 
              padding: 20px 50px; 
              font-size: 22px; 
              font-weight: 800; 
              color: #0f172a; 
              text-decoration: none; 
              box-shadow: 0 10px 30px rgba(31, 38, 135, 0.2); 
              transition: all 0.3s; 
              font-family: 'Pretendard', sans-serif;">
        ✈️ BOOK YOUR OSAKA NOW
    </a>
</div>
""", unsafe_allow_html=True)