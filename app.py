from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
favorites = []

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
        'https://api.spoonacular.com/recipes/complexSearch',
        params={'query': query, 'apiKey': API_KEY}
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipes"}), response.status_code

    data = response.json()
    
    return jsonify(data)

@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_detail(recipe_id):
    response = requests.get(
        f'https://api.spoonacular.com/recipes/{recipe_id}/information',
        params={'apiKey': API_KEY}
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipe details"}), response.status_code

    data = response.json()
    return jsonify(data)

@app.route('/save-favorite/<int:recipe_id>', methods=['POST'])
def save_favorite(recipe_id):
    # Simulate saving the recipe to a database or list
    if recipe_id not in favorites:
        favorites.append(recipe_id)
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'Recipe already in favorites'}), 400

if __name__ == '__main__':
    app.run(debug=True)
