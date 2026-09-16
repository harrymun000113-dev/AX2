from flask import Flask, render_template, jsonify
import webbrowser
from threading import Timer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 1. 당근마켓 기능
@app.route('/api/danggeun', methods=['POST'])
def run_danggeun():
    # TODO: Appium 연동 (당근마켓 채팅 반자동)
    return jsonify({"status": "success", "message": "✅ 당근마켓 채팅 전송 완료!"})

# 2. 사진 리사이징 기능
@app.route('/api/resize', methods=['POST'])
def run_resize():
    # TODO: Pillow 연동 (L, R, M 사진 리사이징)
    return jsonify({"status": "success", "message": "✅ 부품별 이미지 리사이징 완료!"})

# 3. 번개장터 업로드 기능
@app.route('/api/bunjang', methods=['POST'])
def run_bunjang():
    # TODO: Playwright 연동 (번개장터 업로드)
    return jsonify({"status": "success", "message": "✅ 번개장터 3건 자동 업로드 완료!"})

# 4. 구글 시트 동기화 기능
@app.route('/api/sheet', methods=['POST'])
def run_sheet():
    # TODO: gspread 연동 (구글 시트 재고/수익 관리)
    return jsonify({"status": "success", "message": "✅ 재고 및 수익 시트 동기화 완료!"})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)