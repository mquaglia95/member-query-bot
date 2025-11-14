import faiss
import json
import os
from sentence_transformers import SentenceTransformer

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
    """Generate answer from retrieved messages."""
    if not relevant_messages:
        return "I couldn't find any relevant information in the messages to answer your question."
    
    # For now, return a formatted response with the most relevant messages
    # TODO: Integrate LLM for more natural language generation
    
    best_match = relevant_messages[0]
    
    # If the best match is very close (low distance), use it directly
    if best_match['distance'] < 0.5:
        return f"{best_match['user_name']} said: \"{best_match['message']}\""
    
    # Otherwise, show top 3 relevant messages
    context_parts = []
    for i, msg in enumerate(relevant_messages[:3], 1):
        context_parts.append(f"{i}. {msg['user_name']}: {msg['message']}")
    
    context = "\n".join(context_parts)
    
    return f"Here are the most relevant messages I found:\n\n{context}\n\n(Note: LLM integration coming soon for more natural answers)"

def answer_question(question: str):
    """Main function to answer a question."""
    if not index:
        return "Error: Embeddings not built. Please run 'python run_embeddings.py' first."
    
    relevant_messages = retrieve_relevant_messages(question)
    answer = generate_answer(question, relevant_messages)
    
    return answer