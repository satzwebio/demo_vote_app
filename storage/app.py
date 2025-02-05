from flask import Flask, render_template, request, redirect
import os
import uuid
import psycopg2

app = Flask(__name__, static_folder='static')

# Define upload directory (Mounted PVC path)
UPLOAD_FOLDER = "/mnt/filesystem-pvc"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database Configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "db"), 
    "port": os.getenv("DB_PORT", "5432")
}

# Setup DB connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Home route
@app.route('/')
def index():
    try:
        # Fetch colors from DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, color FROM colors")
        colors = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        colors = [("Error connecting to DB", str(e))]

    # List files in PVC directory and calculate file size in KB
    try:
        files = [{"name": f, "size": os.path.getsize(os.path.join(UPLOAD_FOLDER, f)) // 1024} for f in os.listdir(UPLOAD_FOLDER)]
    except Exception as e:
        files = [{"name": "Error reading files", "size": str(e)}]

    return render_template('index.html', colors=colors, files=files)

@app.route('/add', methods=['POST'])
def add_color():
    color = request.form.get('color')
    if color:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            random_id = str(uuid.uuid4())
            cur.execute("INSERT INTO colors (id, color) VALUES (%s, %s)", (random_id, color))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return f"Database error: {e}", 500
    return redirect('/')

@app.route('/delete/<color_id>', methods=['POST'])
def delete_color(color_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM colors WHERE id = %s", (color_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Database error: {e}"
    return redirect('/')

# File Upload Route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save file to the PVC
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Reload file list to reflect the new file
    return redirect('/')

# File Delete Route
@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        # Remove file from PVC
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return f"Error deleting file: {e}", 500
    
    # Reload the page after deletion
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
