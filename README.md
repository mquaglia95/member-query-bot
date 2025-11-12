# **This project is under development**

# **memberQueryBot**

A **question-answering assistant** for member data.  
This API allows you to ask natural-language questions about members (e.g., “When is Layla planning her trip to London?”) and returns answers inferred from the member messages dataset.

It uses **vector embeddings** for retrieval and a **local LLM** for generating answers, fully free and locally deployable.

---

## **Features**

- Retrieve relevant member messages using **FAISS** + **SentenceTransformers**
- Generate answers using a **local LLM** (Ollama or any compatible local model)
- Single API endpoint: `/ask`
- Fully free to run — no paid APIs required
- Easy to extend to new datasets

---

## **Getting Started**

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/memberQueryBot.git
cd memberQueryBot
