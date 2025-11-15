import faiss
import json
import os
from sentence_transformers import SentenceTransformer
import requests

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

# Load resources on module import
if os.path.exists("app/vector_index.pkl"):
    index = faiss.read_index("app/vector_index.pkl")
    with open("app/indexed_messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
    model = SentenceTransformer(MODEL_NAME)
    print(f"✅ Loaded {len(messages)} messages and FAISS index")
else:
    index = None
    messages = []
    model = None
    print("⚠️ Warning: Embeddings not built. Run 'python run_embeddings.py' first.")

def retrieve_relevant_messages(question: str, k: int = TOP_K):
    """Retrieve top-k most relevant messages for a question."""
    if not index or not model:
        return []
    
    q_emb = model.encode([question], convert_to_numpy=True)
    distances, indices = index.search(q_emb, k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(messages):
            results.append({
                "message": messages[idx]["message"],
                "user_name": messages[idx].get("user_name", "Unknown"),
                "timestamp": messages[idx].get("timestamp", ""),
                "distance": float(distances[0][i])
            })
    
    return results

def generate_answer(question: str, relevant_messages: list):
    """Generate answer using Ollama LLM with retrieved messages as context."""
    if not relevant_messages:
        return "I couldn't find any relevant information in the messages to answer your question."
    
    # Build context from top 5 most relevant messages
    context_parts = []
    for msg in relevant_messages[:5]:
        context_parts.append(f"- {msg['user_name']}: {msg['message']}")
    
    context = "\n".join(context_parts)
    
    # Create prompt for LLM
    prompt = f"""You are a helpful assistant that answers questions based on the provided member messages.

Member Messages:
{context}

Question: {question}

Instructions:
- Answer the question directly and concisely using ONLY information from the messages above
- If the answer is not in the messages, say "I couldn't find that information in the messages"
- Be specific - include names, dates, locations, or numbers when relevant
- Keep your answer brief (1-2 sentences)

Answer:"""
    
    try:
        # Call Ollama API
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                'model': 'llama3.2',
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json()['response'].strip()
            return answer
        else:
            return f"Error: Could not generate answer (status {response.status_code})"
            
    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Please start Ollama service."
    except requests.exceptions.Timeout:
        return "Error: Answer generation timed out."
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def answer_question(question: str):
    """Main function to answer a question."""
    if not index:
        return "Error: Embeddings not built. Please run 'python run_embeddings.py' first."
    
    relevant_messages = retrieve_relevant_messages(question)
    answer = generate_answer(question, relevant_messages)
    
    return answer