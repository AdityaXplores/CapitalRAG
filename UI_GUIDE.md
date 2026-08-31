# Streamlit Web UI Guide

The **web UI** (`app.py`) provides a modern, interactive interface for the RAG system.

## 🚀 Quick Start

```bash
# 1. Install dependencies (if not already done)
pip install -r requirements.txt

# 2. Make sure you've ingested data
python ingest.py

# 3. Start the Streamlit app
streamlit run app.py
```

The UI will open at `http://localhost:8501` in your browser.

---

## 📖 Features & Modes

### 💬 Chat (Full RAG)
**Main Q&A interface** — Ask questions and get cited answers.

**What it does:**
- Embeds your question using local embeddings
- Retrieves the top-k most relevant chunks
- Sends context + question to the selected LLM (DeepSeek/OpenAI/Claude)
- Returns a grounded answer with inline citations

**Tips:**
- Questions like *"What is tracking error?"* work great
- The model will refuse to answer if the data doesn't contain the information
- Enable "Show retrieved chunks" in settings to see what context was used

### 🔎 Search Preview
**Retrieval-only demo** — See chunks without LLM generation (no API cost).

**What it does:**
- Searches the vector store for relevant chunks
- Shows relevance scores (0-100%)
- Displays chunk source type (metric, table, or text)
- **No LLM involved** — completely free to run

**Use case:** Verify what data exists before asking a question, or debug retrieval quality.

### 📤 Upload Documents
**Expand the knowledge base** — Add new PDFs or YAML files.

**How it works:**
1. Select PDF or YAML files from your computer
2. Click "Save to data/ folder"
3. Files are written to `data/docs/` (PDFs) or `data/` (YAML)
4. Run `python ingest.py` in terminal to embed and ingest
5. Restart Streamlit or wait for auto-reload to see new data

**File types:**
- **PDF** — Narrative text + tables (automatically extracted)
- **YAML** — Metric definitions with versions

### 📋 Chat History
**Track all your conversations** — View, inspect, and export.

**Features:**
- Shows all questions asked and answers received
- Timestamps for each conversation
- **Export as JSON** — Download your entire chat history as a JSON file
- Most recent conversations shown first

---

## ⚙️ Settings

Located in the **Settings** expander in the sidebar:

| Setting | Default | What it does |
|---------|---------|------|
| **Top-K chunks** | 6 | How many chunks to retrieve. Higher = broader context, slower response. |
| **Show retrieved chunks** | ✓ | Display the chunks used to answer, with source badges. |

---

## 🎨 UI Elements Explained

### Source Badges
Each retrieved chunk is tagged by source type:

- **📋 METRIC v1.2** — Governed metric definition (with version)
- **📊 TABLE - page 5** — Extracted table (with page number)
- **📄 TEXT** — Narrative prose from PDF

### Relevance Score (Search Preview only)
Shows how similar each chunk is to your search (0-100%).
- **90-100%** — Highly relevant
- **70-89%** — Relevant
- **<70%** — Loosely relevant

---

## 🔧 Troubleshooting

### "Connection refused" or "Cannot connect to server"
- Make sure you ran `python ingest.py` first
- Verify `chroma_db/` folder exists with data

### Questions return "I don't have that in the provided data"
- The model is correctly refusing out-of-scope questions
- Use **Search Preview** to verify relevant chunks exist
- If not, upload more documents and re-run `python ingest.py`

### UI not updating after document upload
- Manually restart Streamlit: `Ctrl+C` → `streamlit run app.py`
- Or click the "Rerun" button in the Streamlit UI

### "API key not set"
- Copy `.env.example` to `.env`
- Fill in your API key for the selected provider
- Restart Streamlit

---

## 🌐 Deployment

### Local Network (share with teammates)
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Then others can access: `http://<your-ip>:8501`

### Public Cloud (Streamlit Cloud)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy

---

## 📊 Performance Tips

- **Top-K = 3-6** for fast responses
- **Top-K = 10-20** for comprehensive answers
- **Search Preview** is instant (no API calls)
- **Chat mode** depends on LLM latency (typically 2-10 seconds)

---

## 🔗 Integration with CLI

You can also use the system via command line:

```bash
# CLI interactive Q&A
python ask.py

# One-off answer
python -c "from rag import answer; print(answer('your question here'))"

# Retrieval preview (CLI)
python query.py "your question"
```

**The web UI is recommended for best user experience!**
