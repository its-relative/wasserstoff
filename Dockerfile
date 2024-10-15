# Base image with Python 3.10
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose any necessary ports (if your app interacts with the outside world)
# EXPOSE 8000  # Uncomment if you have a web server running on port 8000

# Set environment variables (optional)
# ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python3", "main.py"]
