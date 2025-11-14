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

## Getting Started

### **1. Clone the repository**
```bash
git clone https://github.com/mquaglia95/memberQueryBot.git
cd memberQueryBot
```

### **2. Set up virtual environment (recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Fetch member messages from API**
```bash
python app/swaggerDataFetcher.py
```

This will download all member messages from the API and save them to `app/messages.json`.

### **5. Build embeddings and FAISS index**
```bash
python run_embeddings.py
```

This generates vector embeddings for all messages and creates a FAISS index for fast retrieval. This step may take 2-5 minutes on first run.


## **Exploratory Data Analysis**

** fill in results **

