import os
from flask import Flask, render_template, jsonify, request
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# HARDCODED API KEY: Paste your actual key inside the quotation marks below
client = OpenAI(api_key="YOUR_ACTUAL_API_KEY_HERE")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    menu_items = [
        {"id": "d1", "name": "Strawberry Parfait", "desc": "A delightful blend of strawberry smoothie topped with rich whipped cream.", "image": "음료 사진/딸기 파르페.jpg", "price": 6.50},
        {"id": "d2", "name": "Hot Matcha Latte", "desc": "A comforting, warm cup of premium matcha green tea.", "image": "음료 사진/맛차 라떼.jpg", "price": 5.50},
        {"id": "d3", "name": "Sparkling Lemonade", "desc": "Crisp, refreshing lemonade with sparkling water.", "image": "음료 사진/레몬에이드.jpg", "price": 5.00},
        {"id": "d4", "name": "Classic Soy Milk", "desc": "Smooth, nutty, and lightly sweetened iced soy milk.", "image": "음료 사진/소이 밀크.jpg", "price": 4.50},
        {"id": "s1", "name": "Classic Scones", "desc": "Warm, buttery scones paired perfectly with your favorite drink.", "image": "디저트 사진/스콘 .jpg", "price": 4.00},
        {"id": "s2", "name": "Matcha Basque Cheesecake", "desc": "Rich, creamy basque cheesecake with a deep matcha flavor.", "image": "디저트 사진/바스크치즈 녹차 케이크.jpg", "price": 6.50},
        {"id": "s3", "name": "Tiramisu", "desc": "Classic Italian dessert layered with coffee-soaked ladyfingers.", "image": "디저트 사진/티라미수.jpg", "price": 6.50}
    ]
    return render_template("menu.html", drinks=menu_items)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, cute robot assistant at an automated cafe. Keep answers short, friendly, and helpful. If asked for tissue or straws, say 'I will dispatch a robot to your table!'"},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return jsonify({"reply": "Beep boop! Connection fuzzy."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)