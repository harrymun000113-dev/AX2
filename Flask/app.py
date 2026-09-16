import os
import random
from flask import Flask, render_template, jsonify
import requests

# Get absolute path of directory containing app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# --- STRICT CACHE BUSTING ---
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- ROUTES ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book")
def book():
    return render_template("book.html")

# --- API ENDPOINTS ---
@app.route("/api/fortune")
def get_fortune():
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            data = response.json()
            advice = data.get("slip", {}).get("advice", "Good fortune comes to those who wait!")
            return jsonify({"status": "success", "advice": advice})
    except Exception as e:
        print("Fortune API Error:", e)
    return jsonify({"status": "error", "advice": "Believe in yourself and good things will follow."})

@app.route("/api/book")
def get_book():
    try:
        queries = [
            "subject:fiction", "subject:mystery", "subject:classics", 
            "subject:adventure", "subject:fantasy", "subject:thriller"
        ]
        search_query = random.choice(queries)
        start_index = random.randint(0, 100)
        
        url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&langRestrict=en&maxResults=40&startIndex={start_index}"
        response = requests.get(url)
        
        if response.status_code == 200:
            items = response.json().get("items", [])
            valid_books = []
            for item in items:
                info = item.get("volumeInfo", {})
                images = info.get("imageLinks", {})
                if images.get("thumbnail") and info.get("description"):
                    valid_books.append(info)
            
            if valid_books:
                book_data = random.choice(valid_books)
                title = book_data.get("title", "Unknown Title")
                genre_list = book_data.get("categories", ["General Fiction"])
                genre = genre_list[0] if genre_list else "General Fiction"
                
                description = book_data.get("description", "")
                if len(description) > 150:
                    description = description[:147] + "..."
                    
                cover = book_data.get("imageLinks", {}).get("thumbnail", "").replace("http:", "https:")
                
                return jsonify({
                    "status": "success",
                    "title": title,
                    "genre": genre.upper(),
                    "description": description,
                    "cover": cover
                })
    except Exception as e:
        print("Book API Error:", e)
        
    fallbacks = [
        {
            "title": "The Metamorphosis",
            "genre": "CLASSICS",
            "description": "A salesman wakes up one morning to find himself transformed into a giant insect.",
            "cover": "https://covers.openlibrary.org/b/id/12625257-L.jpg" 
        },
        {
            "title": "Frankenstein",
            "genre": "HORROR",
            "description": "A scientist creates a living creature from the parts of the dead, with disastrous results.",
            "cover": "https://covers.openlibrary.org/b/id/12648054-L.jpg"
        },
        {
            "title": "Alice's Adventures",
            "genre": "FANTASY",
            "description": "A young girl falls down a rabbit hole into a fantastical world full of strange characters.",
            "cover": "https://covers.openlibrary.org/b/id/12818862-L.jpg"
        }
    ]
    
    selected = random.choice(fallbacks)
    return jsonify(selected)

if __name__ == "__main__":
    app.run(debug=True, port=5000)