from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuración de la clave secreta para las sesiones
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria para la sesión

# Ruta para el inicio (index.html)
# Redirige a la página de inicio si el usuario está autenticado, de lo contrario, redirige a la página de inicio de sesión.
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

# Ruta para mostrar recetas

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes")
    recipes = cur.fetchall()
    conn.close()
    return render_template('recipes.html', recipes=recipes)

# Ruta para buscar recetas
# Muestra todas las recetas almacenadas en la base de datos si el usuario está autenticado,
# de lo contrario, redirige a la página de inicio de sesión. Devuelve los resultados en formato JSON.
@app.route('/search')
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE name LIKE ?", ('%' + query + '%',))
    recipes = cur.fetchall()
    conn.close()
    return jsonify([dict(recipe) for recipe in recipes])

# Ruta para añadir una receta (GET muestra el formulario, POST maneja el envío)
# Muestra un formulario para añadir una nueva receta si el usuario está autenticado.
# Maneja el envío del formulario y guarda la nueva receta en la base de datos.
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        ingredients = request.form.getlist('ingredients[]')
        quantities = request.form.getlist('quantities[]')
        step_numbers = request.form.getlist('step_numbers[]')
        step_descriptions = request.form.getlist('step_descriptions[]')

        conn = sqlite3.connect('recipes.db')
        cur = conn.cursor()
        
        # Inserta la receta
        cur.execute("INSERT INTO recipes (name, description) VALUES (?, ?)", (name, description))
        recipe_id = cur.lastrowid

        # Inserta los datos de la receta
        for step_number, ingredient, quantity, step_description in zip(step_numbers, ingredients, quantities, step_descriptions):
            cur.execute("INSERT INTO recipe_details (recipe_id, step_number, ingredient, quantity, step_description) VALUES (?, ?, ?, ?, ?)",
                        (recipe_id, step_number, ingredient, quantity, step_description))
        
        conn.commit()
        conn.close()
        return redirect(url_for('recipes'))
    
    return render_template('add_recipe.html')

# Ruta para mostrar detalles de una receta
# Muestra los detalles de una receta, incluidos los ingredientes y pasos,
# si el usuario está autenticado. De lo contrario, redirige a la página de inicio de sesión.
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Obtén la receta
    cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cur.fetchone()
    
    # Obtén los detalles de la receta
    cur.execute("SELECT * FROM recipe_details WHERE recipe_id = ?", (recipe_id,))
    details = cur.fetchall()
    
    conn.close()
    
    return render_template('recipe_detail.html', recipe=recipe, details=details)

# Ruta para mostrar el formulario de inicio de sesión
# Muestra un formulario para que el usuario inicie sesión.
# Si las credenciales son correctas, inicia la sesión del usuario y lo redirige al inicio.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('recipes.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

# Ruta para mostrar el formulario de registro
# Muestra un formulario para que el usuario se registre en la aplicación.
# Si el registro es exitoso, redirige al usuario a la página de inicio de sesión.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('recipes.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Registro exitoso. Puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso', 'danger')
        conn.close()

    return render_template('register.html')

# Ruta para cerrar sesión
# Elimina los datos de la sesión y redirige al usuario a la página de inicio de sesión.
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

# Ruta para la página "About Us"
# Muestra información sobre la aplicación o el equipo de desarrollo.
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para la página "Contact Us"
# Muestra un formulario de contacto o información para contactar con los desarrolladores.
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ruta para la página "Temporizador"
# Muestra una página con un temporizador (posiblemente para uso en cocina).
@app.route('/temporizador')
def temporizador():
    return render_template('temporizador.html')
