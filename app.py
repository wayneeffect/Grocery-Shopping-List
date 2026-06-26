from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

def init_db():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY, 
                  name TEXT NOT NULL, 
                  quantity TEXT, 
                  category TEXT, 
                  completed INTEGER DEFAULT 0, 
                  added_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_stats():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    # Total items
    c.execute("SELECT COUNT(*) FROM items")
    total = c.fetchone()[0]
    # Completed
    c.execute("SELECT COUNT(*) FROM items WHERE completed = 1")
    completed = c.fetchone()[0]
    # By category
    c.execute("SELECT category, COUNT(*) as count FROM items GROUP BY category")
    categories = dict(c.fetchall())
    conn.close()
    return {
        'total': total,
        'completed': completed,
        'pending': total - completed,
        'completion_rate': round((completed / total * 100) if total > 0 else 0, 1),
        'categories': categories
    }

@app.route('/')
def index():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY completed ASC, added_date DESC")
    items = c.fetchall()
    conn.close()
    stats = get_stats()
    return render_template('index.html', items=items, stats=stats)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('index'))  # Simple validation
    quantity = request.form.get('quantity', '1').strip()
    category = request.form.get('category', 'Other')
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("""INSERT INTO items (name, quantity, category, completed, added_date) 
                 VALUES (?, ?, ?, 0, ?)""",
              (name, quantity, category, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:item_id>')
def complete(item_id):
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("UPDATE items SET completed = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uncomplete/<int:item_id>')
def uncomplete(item_id):
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("UPDATE items SET completed = 0 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    conn = sqlite3.connect('grocery.db')
    c = conn.cursor()
    c.execute("DELETE FROM items")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
