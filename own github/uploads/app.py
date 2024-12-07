import sqlite3
from datetime import datetime

# Veritabanı bağlantısı kurma ve tablo oluşturma
def create_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_db()

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row  # Bu, veritabanı sonuçlarının sözlük gibi olmasını sağlar
    return conn

# Ana sayfa, notları listeleme
@app.route('/')
def index():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

# Yeni not ekleme sayfası
@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        conn.execute('INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)',
                     (title, content, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_note.html')

# Not düzenleme sayfası
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute('UPDATE notes SET title = ?, content = ? WHERE id = ?',
                     (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_note.html', note=note)

# Not silme işlemi
@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


import webbrowser
import threading
from app import app  # Flask uygulamanızın bulunduğu dosya
def run_flask():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    app.run(debug=True)


    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    threading.Thread(target=run_flask).start()

