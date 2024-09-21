# Dockerfile
FROM python:3.11

WORKDIR /app

# Copy your Python files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH /app

# Open streamlit port
EXPOSE 8501 

# Set the default command to run the scheduler
CMD ["python", "src/run.py"]