# Use a minimal Python image
FROM python:3.11-slim

# Install dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/local/app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 80

# Run the application with Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--workers", "4"]
