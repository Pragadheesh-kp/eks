from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Read from environment variables
DB_NAME = os.getenv("DB_NAME", "cruddb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "crudpass")
DB_HOST = os.getenv("DB_HOST", "localhost")

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);")
conn.commit()

@app.route('/')
def home():
    return "Welcome to the 3-Tier CRUD Application!"

@app.route('/api/items', methods=['GET'])
def get_items():
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

@app.route('/api/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    cursor.execute("INSERT INTO items (name) VALUES (%s) RETURNING id, name;", (data['name'],))
    item = cursor.fetchone()
    conn.commit()
    return jsonify({'id': item[0], 'name': item[1]})

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    cursor.execute("UPDATE items SET name=%s WHERE id=%s RETURNING id, name;", (data['name'], item_id))
    item = cursor.fetchone()
    conn.commit()
    return jsonify({'id': item[0], 'name': item[1]})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor.execute("DELETE FROM items WHERE id=%s;", (item_id,))
    conn.commit()
    return '', 204

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (username, password))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': user_id, 'username': username}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({'error': 'Username a lready e xists'}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
