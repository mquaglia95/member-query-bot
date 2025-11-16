# Stage 1: Build dependencies
FROM python:3.10-slim as builder

WORKDIR /app

# Install build tools if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=wheelhouse -r requirements.txt

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /app/wheelhouse /wheelhouse
RUN pip install --no-cache-dir --find-links=/wheelhouse -r requirements.txt

# Copy application code
COPY app ./app
COPY run_embeddings.py .
COPY app/messages.json ./app/messages.json
COPY app/vector_index.pkl ./app/vector_index.pkl
COPY app/indexed_messages.json ./app/indexed_messages.json
COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]
