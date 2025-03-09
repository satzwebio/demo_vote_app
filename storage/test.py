import subprocess
import os

def generate_large_file_with_data(file_path, file_size_mb):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Create a sample string to repeat and fill the file
        data_to_write = "This is a test line of data. "  # You can change this as needed.
        # Make the string sufficiently long (longer than 1MB to fill more space per write)
        data_to_write = data_to_write * 1024  # This creates a ~1KB chunk per repetition.

        # Calculate the number of times the data should be written to reach the desired file size
        num_repeats = (file_size_mb * 1024) // len(data_to_write)  # Number of repetitions needed

        # Open the file and write the data in chunks to reach the target size
        with open(file_path, "w") as file:
            for _ in range(num_repeats):
                file.write(data_to_write)  # Write the actual data chunk
        print(f"File {file_path} generated successfully with {file_size_mb}MB of real data.")

    except Exception as e:
        print(f"Error generating file: {e}")

# Example usage
generate_large_file_with_data("/mnt/perf-pvc/testfile.txt", 15000)  # 15GB file, change size as needed
