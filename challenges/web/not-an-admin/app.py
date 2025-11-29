# /// script
# dependencies = [
#   "flask"
# ]
# ///
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import functools

app = Flask(__name__)
app.secret_key = 'super_secret_hello_kitty_key'
DATABASE = 'database.db'
FLAG = 'flag{cUt3_p1nk_fl4g_f0r_y0u}'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        ''')
        # Create a default admin user if not exists
        try:
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                       ('admin', generate_password_hash('admin'), 'admin'))
            db.commit()
        except sqlite3.IntegrityError:
            pass
        db.commit()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if not user or user['role'] != 'admin':
            flash('Access denied. Admins only!', 'error')
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('login'))

        flash(error, 'error')

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html', flag=FLAG)

@app.route('/admin/users', methods=('GET', 'POST'))
def manage_users():
    db = get_db()
    if request.method == 'POST':
        user_id = request.form['user_id']
        new_role = request.form['role']
        db.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
        db.commit()
        flash('User role updated successfully!', 'success')

    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('manage_users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
