# 🚀 RAG Toy | Investment Knowledge Base

A **Retrieval-Augmented Generation (RAG)** system for answering questions about investment reports and financial metric definitions using **grounded, cited, and source-aware responses**.

The project combines **vector search, local embeddings, PDF table extraction, governed financial metrics, and LLMs** to create a small but practical investment knowledge assistant.

---

## 📝 Description

**RAG Toy** is a deliberately simple and readable implementation of a Retrieval-Augmented Generation pipeline.

It allows users to ask questions about investment reports and receive answers based **only on the information available in the provided knowledge base**.

The system combines two sources of knowledge:

- 📊 **Governed Metrics** — Versioned financial definitions such as *Tracking Error* and *Sharpe Ratio*.
- 📄 **Investment Reports** — Narrative content and financial tables extracted from PDF annual reports.

Every generated answer includes **source citations**, while questions that cannot be answered from the available information are explicitly refused.

---

## ✨ Key Features

- 🤖 **Retrieval-Augmented Generation**  
  Retrieves relevant information before sending context to the LLM.

- 📚 **Grounded Answers**  
  The model is instructed to answer only from retrieved source material.

- 🔖 **Source Citations**  
  Retrieved facts are tagged with their originating document or metric definition.

- 📊 **Table-Aware PDF Processing**  
  Uses `pdfplumber` to reconstruct financial tables instead of relying only on plain-text extraction.

- 🧮 **Governed Financial Metrics**  
  Stores canonical metric definitions separately with version information.

- 🛡️ **Hallucination Control**  
  Questions outside the knowledge base return:
  > `I don't have that in the provided data.`

- 🔌 **Provider-Agnostic LLM**  
  Supports multiple LLM providers through a common `complete()` interface.

- 🧠 **Local Embeddings**  
  Uses `all-MiniLM-L6-v2` locally through ChromaDB, requiring no embedding API key.

- 💻 **Streamlit Web Interface**  
  Provides an interactive interface for chatting, searching, uploading documents, and viewing history.

- 🔍 **Retrieval vs RAG Comparison**  
  Includes a comparison tool demonstrating the difference between raw retrieval and LLM-generated answers.

---

## 🏗️ How It Works

```text
                         KNOWLEDGE BASE
                              │
              ┌───────────────┴────────────────┐
              │                                │
       metrics.yaml                     PDF Reports
              │                                │
              │                         ┌──────┴──────┐
              │                         │             │
              │                       Prose         Tables
              │                       pypdf       pdfplumber
              │                         │             │
              └───────────────┬─────────┴─────────────┘
                              │
                         Chunk + Embed
                              │
                    all-MiniLM-L6-v2
                              │
                              ▼
                       ChromaDB
                    Vector Database
                              │
                              │
Question ────────► Embedding ────────► Similarity Search
                                           │
                                           ▼
                                    Top-K Chunks
                                           │
                                           ▼
                                  Cited Context
                                           │
                                           ▼
                                     LLM Provider
                                           │
                                           ▼
                                    Grounded Answer
```

### 🔄 RAG Pipeline

**1. Retrieval**

The user's question is converted into an embedding using the same local embedding model used during ingestion.

The system retrieves the most relevant chunks from ChromaDB.

**2. Augmentation**

The retrieved chunks are combined into a context block.

Each chunk contains source information such as:

```text
[source: annual_report.pdf, page 42]
```

**3. Generation**

The selected LLM receives:

```text
System Rules
     +
Retrieved Context
     +
User Question
```

The model then generates an answer using only the provided context.

---

## 🛠️ Tech Stack

### 🐍 Core

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

### 🧠 RAG & AI

![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented_Generation-4B8BBE?style=for-the-badge)
![DeepSeek](https://img.shields.io/badge/DeepSeek-LLM-000000?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-LLM-412991?style=for-the-badge&logo=openai&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-LLM-D97757?style=for-the-badge&logo=anthropic&logoColor=white)

### 🗄️ Vector Database & Embeddings

![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF9900?style=for-the-badge)
![MiniLM](https://img.shields.io/badge/MiniLM-Local_Embeddings-4B8BBE?style=for-the-badge)

### 📄 Document Processing

![PyPDF](https://img.shields.io/badge/pypdf-PDF_Extraction-DC2626?style=for-the-badge)
![pdfplumber](https://img.shields.io/badge/pdfplumber-Table_Extraction-2563EB?style=for-the-badge)

### 🌐 Web Interface

![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## 📁 Project Structure

```text
rag-investment-kb/
│
├── 📄 ingest.py
│   └── Builds the vector database from metrics and PDF documents
│
├── 🔍 query.py
│   └── Retrieval-only interface — no LLM required
│
├── 🤖 rag.py
│   └── Complete RAG pipeline: Retrieval + Augmentation + Generation
│
├── 🧠 llm.py
│   └── Provider-independent LLM interface
│
├── 💬 ask.py
│   └── Interactive command-line Q&A
│
├── 🌐 app.py
│   └── Streamlit web application
│
├── 🧪 test_a.py
│   └── Non-interactive smoke tests
│
├── 📊 review/
│   └── compare_search_vs_rag.py
│       └── Compares retrieval-only vs full RAG
│
├── 📂 data/
│   ├── metrics.yaml
│   │   └── Governed and versioned metric definitions
│   │
│   └── docs/
│       └── PDF investment reports
│
├── 🗄️ chroma_db/
│   └── Local ChromaDB vector store
│
├── 📄 requirements.txt
├── 🔐 .env.example
└── 📖 README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd rag-investment-kb
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the LLM Provider

Create your environment file:

```bash
cp .env.example .env
```

Then configure:

```env
RAG_PROVIDER=deepseek
```

and provide the corresponding API key.

Supported providers:

```text
deepseek
openai
claude
```

Only the selected provider requires an API key.

---

## 📥 Add Documents

Place your PDF investment reports inside:

```text
data/docs/
```

For example:

```text
data/
├── metrics.yaml
└── docs/
    └── annual_report.pdf
```

> ⚠️ The repository does not bundle the example annual report. You can add your own supported PDF documents.

---

## ⚙️ Build the Knowledge Base

Run ingestion once after adding or changing documents:

```bash
python ingest.py
```

The ingestion pipeline:

```text
PDF / Metrics
      ↓
Document Extraction
      ↓
Chunking
      ↓
Local Embeddings
      ↓
ChromaDB
```

Embeddings are generated locally, so ingestion does **not** require an embedding API key.

---

## 🔍 Retrieval-Only Search

You can inspect what the vector database retrieves without using an LLM.

```bash
python query.py "what is tracking error"
```

Multiple questions:

```bash
python query.py \
  "tracking error" \
  "how to calculate sharpe ratio"
```

This is useful for debugging and evaluating the retrieval layer independently.

---

## 🤖 Run the RAG Assistant

Start the interactive CLI:

```bash
python ask.py
```

Example:

```text
Question: What was the funded status, and as of when?

Answer:
The funded status was ... [source: annual_report.pdf, page 42]
```

If the information does not exist in the knowledge base:

```text
I don't have that in the provided data.
```

---

## 🌐 Streamlit Web App

For a graphical interface:

```bash
streamlit run app.py
```

The application provides:

- 💬 Chat-based Q&A
- 🔍 Search preview
- 📄 Document upload
- 🕘 Chat history
- 📚 Source-aware answers

---

## 🧪 Testing

Run the smoke test:

```bash
python test_a.py
```

The test suite includes the expected refusal behavior for questions that cannot be answered from the available knowledge base.

---

## 🔬 Retrieval vs RAG

One of the project's useful demonstrations is the difference between **retrieval** and **generation**.

Run:

```bash
python review/compare_search_vs_rag.py
```

Or provide specific questions:

```bash
python review/compare_search_vs_rag.py \
  "what is tracking error" \
  "what was the funded status?"
```

### Retrieval Only

```text
Question
   ↓
Vector Search
   ↓
Relevant Chunks
```

The user has to interpret the retrieved chunks manually.

### Full RAG

```text
Question
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Context Construction
   ↓
LLM
   ↓
Cited Answer
```

This demonstrates the role of the **Generation** step in RAG.

---

## 📊 Knowledge Sources

The knowledge base contains two different types of information.

### 📐 Governed Metrics

Stored in:

```text
data/metrics.yaml
```

Examples include:

- Tracking Error
- Sharpe Ratio
- Other canonical financial metrics

Each definition can contain a version:

```text
version: 1.0
```

This makes metric definitions traceable and separate from narrative documents.

### 📄 Unstructured Reports

Investment reports can contain:

- Narrative text
- Financial statements
- Tables
- Numerical data
- Definitions
- Investment information

The ingestion pipeline processes both prose and tables separately.

---

## 📑 Table-Aware PDF Extraction

Financial reports often contain tables that are difficult to extract using standard PDF text extraction.

A typical text extractor may produce:

```text
2025  2024  2023  123  456  789
```

without preserving the relationship between labels and values.

This project uses:

```text
pypdf
   │
   └── Narrative text

pdfplumber
   │
   └── Financial tables
           ↓
       Markdown
```

Tables are converted into Markdown-style structures so the LLM can interpret rows and columns more reliably.

---

## 🛡️ Grounding & Hallucination Control

The RAG pipeline uses a strict generation prompt that instructs the LLM to:

1. Use only retrieved context.
2. Avoid introducing unsupported facts.
3. Include source citations.
4. Refuse questions that cannot be answered from the provided context.

Example:

```text
User:
What is the current stock price of Apple?

Knowledge Base:
No information about Apple's stock price.

Assistant:
I don't have that in the provided data.
```

The refusal logic is implemented during **generation**, rather than filtering the question during retrieval.

---

## 🔄 Provider-Agnostic Architecture

The project exposes a common interface:

```python
complete(...)
```

The underlying provider can be switched through `.env`:

```env
RAG_PROVIDER=deepseek
```

or:

```env
RAG_PROVIDER=openai
```

or:

```env
RAG_PROVIDER=claude
```

The RAG pipeline does not need to change when switching providers.

```text
                  ┌─────────────┐
                  │  rag.py     │
                  └──────┬──────┘
                         │
                    complete()
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      DeepSeek         OpenAI         Claude
```

---

## ⚡ Design Decisions

### Why ChromaDB?

ChromaDB provides a lightweight local vector database suitable for a small RAG application without requiring a separate hosted infrastructure.

### Why Local Embeddings?

`all-MiniLM-L6-v2` provides 384-dimensional embeddings locally.

Benefits:

- No embedding API key
- No embedding API cost
- Works offline
- Simple development setup

### Why a Governed Metric Layer?

Financial metric definitions can be sensitive to wording and version.

Keeping them separately in `metrics.yaml` allows the application to distinguish between:

```text
Authoritative Definition
        +
Narrative Report Information
```

### Why Extract Tables Separately?

Financial tables contain relationships between rows, columns, labels, and numbers that can be lost during plain-text PDF extraction.

Dedicated table extraction preserves this structure better.

---

## ⚠️ Limitations

- 📄 PDF extraction is tuned for specific document layouts.
- 🖼️ Scanned/image-only PDFs require OCR and are currently out of scope.
- 🔎 Retrieval quality depends on chunking and embedding quality.
- 📊 Table extraction uses heuristics and may require tuning for different PDF formats.
- 🗄️ The current ingestion process re-embeds the complete dataset.
- 🧹 Removing a source document requires rebuilding `chroma_db/` to remove its old chunks.
- 🔐 LLM responses still depend on the selected provider and model.

---

## 🗺️ Future Improvements

- [ ] Add OCR support for scanned PDFs
- [ ] Add incremental document ingestion
- [ ] Add document deletion and synchronization
- [ ] Improve table extraction across different PDF layouts
- [ ] Add hybrid keyword + vector retrieval
- [ ] Add reranking
- [ ] Add automated retrieval evaluation
- [ ] Add metadata filtering
- [ ] Add more financial report formats
- [ ] Add source-document previews
- [ ] Add authentication and multi-user support

---

## 📸 Example

The project can be demonstrated using the **HOOPP 2025 Annual Report** as an example investment document.

The assistant can answer questions about:

- Financial metrics
- Report values
- Tables
- Dates and reporting periods
- Metric definitions

while attaching source information to retrieved facts.

---

## 💡 What This Project Demonstrates

This project demonstrates practical implementation of:

```text
RAG
├── Document ingestion
├── Text chunking
├── Embeddings
├── Vector databases
├── Similarity search
├── Context augmentation
├── LLM generation
├── Source citations
├── Hallucination control
├── PDF processing
├── Table extraction
└── LLM provider abstraction
```

It is intentionally small enough to understand end-to-end while still demonstrating the core architecture used in production-oriented RAG systems.

---

## 📌 Quick Command Reference

```bash
# Install
pip install -r requirements.txt

# Build vector database
python ingest.py

# Retrieval only
python query.py "what is tracking error"

# Interactive RAG
python ask.py

# Streamlit UI
streamlit run app.py

# Tests
python test_a.py

# Compare retrieval vs RAG
python review/compare_search_vs_rag.py
```

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to:

- Open an issue
- Submit a pull request
- Suggest improvements to retrieval
- Add support for additional document formats
- Improve table extraction

---

> 🚀 **Built to demonstrate a clean, grounded, and understandable RAG pipeline for investment knowledge.**
>
> **Retrieval → Context → Generation → Cited Answer**
