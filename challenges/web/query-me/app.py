# /// script
# dependencies = [
#   "flask"
# ]
# ///
import sqlite3
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection():
    # Open in read-only mode using URI
    # Note: This requires the database file to exist.
    try:
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        print(f"Error connecting to DB: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    sql_query = data.get('query')

    if not sql_query:
        return jsonify({'error': 'No query provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)

        # "get only one row of data at the time"
        row = cursor.fetchone()

        if row:
            # Convert row to dict
            result = dict(row)
            return jsonify({'result': result})
        else:
            return jsonify({'result': None, 'message': 'No results found'})

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
