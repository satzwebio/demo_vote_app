import os
import random
import sys
import uuid
import time

def generate_random_files(size_gb):
    """Generate 10 files of specified size with unique, non-deduplicable content."""
    num_files = 10
    chunk_size = 1024  # 1KB chunks
    size_bytes = size_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    
    for file_num in range(num_files):
        filename = f"random_file_{file_num+1}.dat"
        content = bytearray()
        
        while len(content) < size_bytes:
            # Mix random bytes with unique identifiers
            chunk = bytearray(random.getrandbits(8) for _ in range(chunk_size))
            unique_id = f"{uuid.uuid4()}{time.time_ns()}{random.getrandbits(128)}".encode()
            chunk.extend(unique_id)
            content.extend(chunk[:chunk_size])
            
        # Write exact size to file
        with open(filename, 'wb') as f:
            f.write(content[:size_bytes])
        print(f"Created {filename} ({size_gb}GB)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            size_gb = float(sys.argv[1])
            generate_random_files(size_gb)
        except ValueError:
            print("Please provide a valid number for size in GB")
    else:
        print("Usage: python generate_files.py <size_in_GB>")