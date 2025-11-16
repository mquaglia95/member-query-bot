import json
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading messages...")
with open("app/messages.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Handle paginated response format
if isinstance(data, dict) and "items" in data:
    messages = data["items"]
else:
    messages = data

# Filter out messages with empty text
valid_messages = [m for m in messages if m.get("message", "").strip()]
print(f"Valid messages for embedding: {len(valid_messages)}")

# Extract text for embedding
texts = [msg["message"] for msg in valid_messages]

print(f"Loading embedding model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

print("Generating embeddings...")
embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

print("Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("Saving index and messages...")
faiss.write_index(index, "app/vector_index.pkl")

# Save the valid messages with their indices
with open("app/indexed_messages.json", "w", encoding="utf-8") as f:
    json.dump(valid_messages, f, indent=2, ensure_ascii=False)

print(f"\n✅ SUCCESS!")
print(f"  - Embeddings created for {len(valid_messages)} messages")
print(f"  - FAISS index saved to app/vector_index.pkl")
print(f"  - Indexed messages saved to app/indexed_messages.json")