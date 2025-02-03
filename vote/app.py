from flask import Flask, render_template, request, make_response, g
import os
import socket
import logging
import uuid
import psycopg2



from flask import Blueprint, render_template, request, redirect


option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__, static_folder='static')

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


# DB_CONFIG = {
#     "dbname": "postgres",
#     "user": "postgres",
#     "password": "postgres",
#      "host": "db",  # Change to 'db' if running in Docker
#      "port": 5432
# }

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, vote FROM votes")
        votes = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        votes = [("Error connecting to DB", str(e))]
    return render_template('index.html', votes=votes)

@app.route('/add', methods=['POST'])
def add_message():
    vote = request.form.get('vote')
    if vote:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            print(f"{vote}")
            random_id = str(uuid.uuid4())
            cur.execute("INSERT INTO votes (id,vote) VALUES (%s, %s)", (random_id,vote))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")  # Logs error to the console
            return f"Database error: {e}", 500  # Returns HTTP 500 error for debugging
    return redirect('/')


@app.route('/delete/<vote_id>', methods=['POST'])
def delete_vote(vote_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM votes WHERE id = %s", (vote_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Database error: {e}"
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
