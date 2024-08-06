from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import User
from forms import RegistrationForm, LoginForm
import requests
import os

app = Flask(__name__)
app.secret_key = '0000'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.get(username)

favorites = []

API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
@login_required
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

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorite_recipes = []
    for recipe_id in favorites:
        # Fetch recipe details (you can use a similar method as in fetchRecipeDetails)
        response = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}")
        if response.status_code == 200:
            favorite_recipes.append(response.json())
    return jsonify(favorite_recipes), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get(form.username.data):
            flash('Username already exists.')
        else:
            User(form.username.data, form.password.data)
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
