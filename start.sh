#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 10

# Pull the llama3.2 model
ollama pull llama3.2

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8080