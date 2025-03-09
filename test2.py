import os

def generate_unique_files(size_gb):
    num_files = 10  # Fixed number of files
    file_size = (size_gb * 1024) // num_files  # Each file's size in MB

    files_created = []
    for i in range(1, num_files + 1):
        file_path = os.path.join(UPLOAD_FOLDER1, f"file_{i}.txt")
        try:
            with open(file_path, "w") as f:
                # Writing unique content for each file
                f.write(f"Unique data for file {i} - {os.urandom(64).hex()}")
            files_created.append(file_path)
        except Exception as e:
            return str(e)

    return files_created
