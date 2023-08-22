# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory in Docker
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all source files to the image
COPY . .

# Expose the port your app might run on (if needed)
# EXPOSE some_port

# Command to run your application
CMD ["python3", "src/main.py", "--run_pure"]
