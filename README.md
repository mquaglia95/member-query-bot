# **memberQueryBot**

A **question-answering assistant** for employee data.  
This API allows you to ask natural-language questions about members (e.g., “When is Layla planning her trip to London?”), and the API returns answers inferred from the member messages dataset.

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

### **4. Install and set up Ollama (for LLM-powered answers)**
```bash
# Download and install Ollama from: https://ollama.com/download

# Pull the llama3.2 model
ollama pull llama3.2

# Verify Ollama is running
ollama list
```

### **5. Fetch member messages from API**
```bash
python app/swaggerDataFetcher.py
```

This will download all member messages from the API and save them to `app/messages.json`.

### **6. Build embeddings and FAISS index**
```bash
python run_embeddings.py
```

This generates vector embeddings for all messages and creates a FAISS index for fast retrieval. This step may take 2-5 minutes on first run.

### **7. Run the API**
```bash
uvicorn app.main:app --reload
```

Your API will be running at: `http://127.0.0.1:8000`

### **8. Test the chatbot**

**Using curl (macOS/Linux):**
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "When is Layla planning her trip to London?"}'
```

**Using PowerShell (Windows):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body '{"question": "When is Layla planning her trip to London?"}'
```

**Using browser:**
Navigate to `http://127.0.0.1:8000/docs` for interactive API documentation.


## **Exploratory Data Analysis**

I conducted a comprehensive exploratory data analysis on the member messages dataset to understand its structure, quality, and patterns. The dataset consists of 100 messages from 10 unique users, spanning approximately 12 months from November 2024 to October 2025.

### **Basic Statistics**

The dataset contains 5 columns: `id`, `user_id`, `user_name`, `timestamp`, and `message`. All fields are string/object types with complete data coverage. Message lengths are remarkably consistent, with an average of 64 characters (standard deviation: 9 characters, range: 47-84 characters). This uniformity suggests the messages may follow a template or structured format. User activity is relatively balanced, with the most active user (Sophia Al-Farsi) contributing 16 messages and the least active (Amina Van Den Berg) contributing 5 messages.

### **Dataset Columns**

| Column Name | Description |
|------------|-------------|
| **id** | Unique UUID for each message event. |
| **user_id** | UUID identifying the user who sent the message. |
| **user_name** | Full name of the user. |
| **timestamp** | ISO 8601 timestamp indicating when the message was sent. |
| **message** | The full text content of the user’s message. |

---

### **First 10 Rows of Data**

| id | user_id | user_name | timestamp | message |
|----|---------|-----------|-----------|---------|
| b1e9bb83-18be-4b90-bbb8-83b7428e8e21 | cd3a350e-dbd2-408f-afa0-16a072f56d23 | Sophia Al-Farsi | 2025-05-05T07:47:20.159073+00:00 | Please book a private jet to Paris for this Friday. |
| 609ba052-c9e7-49e6-8b62-061eb8785b63 | e35ed60a-5190-4a5f-b3cd-74ced7519b4a | Fatima El-Tahir | 2024-11-14T20:03:44.159235+00:00 | Can you confirm my dinner reservation at The French Laundry for four people tonight? |
| 44be0607-a918-40fa-a122-b2435fe54f3e | 23103ae5-38a8-4d82-af82-e9942aa4aefb | Armand Dupont | 2025-03-09T02:25:23.159256+00:00 | I need two tickets to the opera in Milan this Saturday. |
| a1579c1b-7f25-4d92-b421-0982f8fbf566 | 5b2e7346-eef5-445d-a063-6c5267f04bf8 | Hans Müller | 2025-08-02T05:20:44.159269+00:00 | Could you check why my recent payment hasn't been processed yet? |
| 43d8a12e-4fdb-4c82-8a78-f7dfff583b9f | fc15e14c-f56f-4137-a7cd-797f90b61c93 | Layla Kawaguchi | 2025-04-10T06:52:16.159280+00:00 | Please remember I prefer aisle seats during my flights. |
| d848fff4-b4e6-4111-8ba8-b5e33ca74d10 | 23103ae5-38a8-4d82-af82-e9942aa4aefb | Armand Dupont | 2025-09-05T16:42:34.159290+00:00 | Can you arrange a private yacht for a weekend in Monaco? |
| 5e0c17ce-5b05-4fa5-a3fe-14c66c79e044 | cd3a350e-dbd2-408f-afa0-16a072f56d23 | Sophia Al-Farsi | 2025-01-21T15:01:42.159300+00:00 | I haven't received the itinerary for my upcoming trip—can you provide an update? |
| 8aa3818a-2f58-41f0-b9c0-0e0b1af22f8a | cd3a350e-dbd2-408f-afa0-16a072f56d23 | Sophia Al-Farsi | 2025-10-07T14:13:39.159309+00:00 | The concert tickets I received were perfect; thank you for arranging everything. |
| a5759130-9354-48cd-a398-949661844fcb | 23103ae5-38a8-4d82-af82-e9942aa4aefb | Armand Dupont | 2025-02-12T05:58:08.159318+00:00 | Please update my profile with my new phone number: 555-349-7841. |
| 4df0ad3b-d73a-45fa-81b5-29f803d54783 | fc15e14c-f56f-4137-a7cd-797f90b61c93 | Layla Kawaguchi | 2025-05-19T13:34:32.159327+00:00 | Book a villa in Santorini for the first week of December. |


---
### Data Quality Summary

#### **Insights and Observations**
**Perfect completeness:** Zero null values, empty fields, or missing data
**Consistent user identity:** No duplicate or conflicting user_id/user_name mappings
**Valid timestamps:** All dates parse correctly with no future timestamps
**High uniformity:** Message lengths and formatting show unusually low variance
**Small dataset:** 100 messages from 10 users limits statistical significance
**Limited time range:** 12-month span may not capture long-term trends
**Some non-ASCII characters present in messages:** 15% of messages contain non-ASCII characters (accented names, international locations)
**Anomalies Identified:**The dataset exhibits fantastic quality with no anomalies, inconsistencies, or data integrity issues detected.
---
### Data Completeness

![Message Length Distribution](app/exploratoryDataAnalysis/analysis_output/message_length.png)

**Key Findings:** The analysis revealed clean, high-quality data with zero null values, empty strings, or whitespace-only entries across all 500 data points (5 columns per row of data). The message length distribution demonstrates a tight clustering around the mean, with most messages falling between 56-69 characters. The box plot confirms minimal outliers, which signifies highly standardized message formatting. This level of consistency is abnormal for natural user-generated content and is due to a constrained input system with synthetic data generation.

---

### User Activity Patterns

![Top 10 Most Active Users](app/exploratoryDataAnalysis/analysis_output/top_users.png)

**Key Findings:** All 10 users in the dataset show active participation, with message counts ranging from 5 to 16. The top three contributors (Sophia Al-Farsi, Fatima El-Tahir, and Hans Müller) account for 42% of total messages. The relatively even distribution implies a small, engaged user base. Each `user_id` maps consistently to exactly one `user_name` with no conflicts, indicating robust identity management.

---

### Content Analysis

![Most Common Words in Messages](app/exploratoryDataAnalysis/analysis_output/word_cloud.png)

**Key Findings:** The word cloud is a visual representation of frequently used words in this data. The messages primarily contain service requests and booking inquiries. Repeatedly used terms include "book" "reservation" "please" "dinner" "ticket" and popular destinations including Paris, Tokyo, and Milan. This confirms that the dataset represents a concierge or luxury service platform where users request travel, dining, and entertainment arrangements.

---

### Temporal Patterns

![Messages Over Time](app/exploratoryDataAnalysis/analysis_output/messages_over_time.png)

**Key Findings:** Message activity is distributed relatively evenly across the timeframe with no significant spikes or gaps. All timestamps are valid with no future dates or parsing errors. The consistent activity pattern suggests either steady user engagement or potentially synthetic data generation. No clear seasonality is evident, though this may be due to the limited sample size (100 messages).

---

### Activity by Day of Week

![Message Distribution by Day of Week](app/exploratoryDataAnalysis/analysis_output/day_of_week.png)

**Key Findings:** Message activity shows variation across days of the week, with Tuesday showing the highest activity with 20 messages and Sunday the lowest with 9 messages. The pattern suggests business-day preference for making requests, with reduced weekend activity.

---

### Activity by Hour of Day

![Message Activity by Hour](app/exploratoryDataAnalysis/analysis_output/hourly_activity.png)

**Key Findings:** Hourly analysis reveals clear activity patterns with peak usage between 14:00-16:00 (afternoon hours). The peak hour is 15:00 with 8 messages, while several hours show zero activity (00:00-06:00), indicating night-time dormancy. The distribution suggests users in similar time zones. This temporal clustering provides insights for optimal service staffing and response time optimization.

---

### Implications for Question-Answering System

The high data quality and consistent formatting make this dataset ideal for building a semantic search and question-answering system. The absence of null values eliminates the need for data cleaning pipelines. The clear service-request pattern (bookings, reservations, travel) provides a well-defined domain for the chatbot to operate within. Message content is sufficiently detailed to enable accurate information extraction for questions about specific users, dates, locations, and service types.