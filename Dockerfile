FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY run_embeddings.py .

# Copy pre-built embeddings and index
COPY app/messages.json ./app/messages.json
COPY app/vector_index.pkl ./app/vector_index.pkl
COPY app/indexed_messages.json ./app/indexed_messages.json

# Expose port
EXPOSE 8080

# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

