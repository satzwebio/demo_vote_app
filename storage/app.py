from flask import Flask, render_template, request, redirect, jsonify
import os
import uuid
import psycopg2

app = Flask(__name__, static_folder='static')

# Define upload directory (dynamically use Git Bash or Windows path)
if os.name == 'nt':  # Check if it's a Windows system
    UPLOAD_FOLDER = r"C:\Users\satzw\OneDrive\Desktop\example-voting-app\mnt-filesystem"
    UPLOAD_FOLDER1 = r"C:\Users\satzw\OneDrive\Desktop\example-voting-app\mnt-filesystem1"
else:
    UPLOAD_FOLDER = "/mnt/filesystem-pvc"  # Adjust this for non-Windows paths (like Docker or Linux)
    UPLOAD_FOLDER1 = "/mnt/perf-pvc"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER1, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# Database Configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"), 
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

@app.route('/file-list')
def file_list():
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({"error": "Upload folder not found", "files": []}), 404

        files = []
        for f in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(file_path):  # Ensure it's a file, not a directory
                files.append({"name": f, "size": os.path.getsize(file_path) // 1024})

        return jsonify(files)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_files(size_gb):
    num_files = 10  # Fixed to 10 files
    file_size = (size_gb * 1024) // num_files  # Each file's size in MB

    files_created = []
    for i in range(1, num_files + 1):
        file_path = os.path.join(UPLOAD_FOLDER1, f"file_{i}.bin")
        try:
            with open(file_path, "wb") as f:
                f.truncate(file_size * 1024 * 1024)  # Creating file of the specified size
            files_created.append(file_path)
        except Exception as e:
            return str(e)
    
    return files_created

@app.route('/generate', methods=['POST'])
def generate():
    try:
        size_gb = int(request.form['size'])
        if size_gb < 1 or size_gb > 50:
            return jsonify({"error": "Please enter a number between 1 and 50"})

        files_created = generate_files(size_gb)

        return jsonify({"files": sorted(os.listdir(UPLOAD_FOLDER1))})
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/file-list1', methods=['GET'])
def file_list1():
    try:
        if not os.path.exists(UPLOAD_FOLDER1):
            return jsonify({"error": "Upload folder not found", "files": []}), 404

        files = sorted(os.listdir(UPLOAD_FOLDER1))  # Sort files by name
        return jsonify(files)
    
    except Exception as e:
        return jsonify({"error": str(e)})        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
