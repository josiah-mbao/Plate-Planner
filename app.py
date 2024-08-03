from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = requests.get(
        f'https://api.spoonacular.com/recipes/complexSearch',
        params={'query': query, 'apiKey': API_KEY}
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipes"}), response.status_code

    data = response.json()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

