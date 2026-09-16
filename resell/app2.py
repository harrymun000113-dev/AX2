from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # 대시보드 HTML 화면을 띄워줍니다.
    return render_template('index.html')

@app.route('/api/danggeun', methods=['POST'])
def run_danggeun():
    # TODO: Appium 연동 코드 작성
    return jsonify({"status": "success", "message": "당근마켓 채팅을 전송했습니다."})

if __name__ == '__main__':
    # 디버그 모드로 로컬 서버 실행
    app.run(debug=True, port=5000)