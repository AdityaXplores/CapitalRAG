"""Streamlit UI for the RAG Investment Knowledge Base system.

Features:
- Interactive Q&A with cited answers
- Chat history tracking
- Retrieval-only search preview
- Document upload for ingestion
- Source chunk inspection
"""
import json
import os
from pathlib import Path
from datetime import datetime

import streamlit as st
import chromadb

from rag import answer as rag_answer
from llm import describe

# Page configuration
st.set_page_config(
    page_title="Investment RAG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .citation {
        background-color: #e8f4f8;
        padding: 10px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9em;
    }
    .source-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: bold;
        margin-right: 8px;
    }
    .source-metric {
        background-color: #fff3cd;
        color: #856404;
    }
    .source-table {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .source-text {
        background-color: #d4edda;
        color: #155724;
    }
    .answer-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .retrieved-box {
        background-color: #f1f3f5;
        padding: 12px;
        margin: 10px 0;
        border-radius: 6px;
        border-left: 3px solid #6c757d;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# Sidebar
with st.sidebar:
    st.title("🔍 RAG Control Panel")
    st.divider()
    
    mode = st.radio(
        "**Select Mode:**",
        ["💬 Chat (Full RAG)", "🔎 Search Preview", "📤 Upload Documents", "📋 Chat History"]
    )
    
    st.divider()
    st.caption(f"**LLM Provider:** {describe()}")
    
    # Settings
    with st.expander("⚙️ Settings"):
        k = st.slider("Top-K chunks to retrieve:", min_value=1, max_value=20, value=6)
        show_chunks = st.checkbox("Show retrieved chunks", value=True)
        st.caption("💡 More chunks = broader context, slower response")


# ============================================================================
# MODE 1: FULL RAG CHAT
# ============================================================================
if mode == "💬 Chat (Full RAG)":
    st.header("💬 Investment Knowledge Q&A")
    st.markdown("Ask questions about the investment firm's reports and metric definitions.")
    
    # Question input
    col1, col2 = st.columns([4, 1])
    with col1:
        question = st.text_input(
            "Ask a question:",
            placeholder="e.g., 'What is tracking error?' or 'What was the funded status and as of when?'",
            key="chat_input"
        )
    
    with col2:
        submit_button = st.button("Ask", use_container_width=True, type="primary")
    
    # Process question
    if submit_button and question:
        with st.spinner("🔄 Retrieving context and generating answer..."):
            try:
                # Get answer
                full_answer = rag_answer(question, k=k)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "question": question,
                    "answer": full_answer
                })
                
                st.success("✅ Answer generated")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                full_answer = None
        
        # Display answer
        if full_answer:
            st.divider()
            st.subheader("Answer:")
            st.markdown(f'<div class="answer-box">{full_answer}</div>', unsafe_allow_html=True)
            
            # Show retrieved chunks if enabled
            if show_chunks:
                st.divider()
                st.subheader("📚 Retrieved Context")
                
                try:
                    # Retrieve chunks for inspection
                    client = chromadb.PersistentClient(path=str(Path(__file__).parent / "chroma_db"))
                    col = client.get_or_create_collection("investment_kb")
                    res = col.query(query_texts=[question], n_results=k)
                    chunks = res["documents"][0]
                    metas = res["metadatas"][0]
                    
                    for i, (chunk, meta) in enumerate(zip(chunks, metas), 1):
                        source = meta.get("source", "unknown")
                        kind = meta.get("type", "unknown")
                        
                        # Badge for source type
                        if kind == "metric":
                            badge_class = "source-metric"
                            badge_text = f"📋 METRIC v{meta.get('version', '?')}"
                        elif kind == "table":
                            badge_class = "source-table"
                            badge_text = f"📊 TABLE - page {meta.get('page', '?')}"
                        else:
                            badge_class = "source-text"
                            badge_text = "📄 TEXT"
                        
                        with st.expander(f"**Chunk {i}:** {source} — {badge_text}"):
                            st.markdown(f'<span class="source-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
                            st.markdown(f'<div class="retrieved-box">{chunk}</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.warning(f"Could not retrieve chunks: {e}")


# ============================================================================
# MODE 2: SEARCH PREVIEW (Retrieval-Only)
# ============================================================================
elif mode == "🔎 Search Preview":
    st.header("🔎 Search Preview (Retrieval Only)")
    st.markdown("See what the vector store retrieves without LLM generation — no API calls.")
    
    search_query = st.text_input(
        "Search the knowledge base:",
        placeholder="e.g., 'Sharpe ratio', 'funded status', 'annual return'",
        key="search_input"
    )
    
    if search_query:
        with st.spinner(f"🔍 Searching for: '{search_query}'..."):
            try:
                client = chromadb.PersistentClient(path=str(Path(__file__).parent / "chroma_db"))
                col = client.get_or_create_collection("investment_kb")
                res = col.query(query_texts=[search_query], n_results=k)
                chunks = res["documents"][0]
                metas = res["metadatas"][0]
                distances = res["distances"][0] if "distances" in res else []
                
                st.success(f"✅ Found {len(chunks)} relevant chunks")
                st.divider()
                
                for i, (chunk, meta, dist) in enumerate(zip(chunks, metas, distances), 1):
                    source = meta.get("source", "unknown")
                    kind = meta.get("type", "unknown")
                    
                    # Determine badge
                    if kind == "metric":
                        badge = f"📋 Metric v{meta.get('version', '?')}"
                        color = "#ffc107"
                    elif kind == "table":
                        badge = f"📊 Table (page {meta.get('page', '?')})"
                        color = "#17a2b8"
                    else:
                        badge = "📄 Text"
                        color = "#28a745"
                    
                    # Similarity score (lower distance = higher similarity)
                    similarity = max(0, 1 - dist) * 100
                    
                    with st.expander(
                        f"**{i}. {source}** — {badge} (Relevance: {similarity:.1f}%)",
                        expanded=(i == 1)
                    ):
                        st.markdown(f'<span class="source-badge" style="background-color: {color}; color: white;">{badge}</span>', unsafe_allow_html=True)
                        st.markdown(f'<div class="retrieved-box">{chunk}</div>', unsafe_allow_html=True)
                        st.caption(f"Source: {source} | Type: {kind}")
            
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")


# ============================================================================
# MODE 3: DOCUMENT UPLOAD & INGESTION
# ============================================================================
elif mode == "📤 Upload Documents":
    st.header("📤 Add Documents to Knowledge Base")
    st.markdown("""
    Upload PDF files or YAML documents to expand the knowledge base.
    - **PDFs:** Prose extracted via pypdf, tables via pdfplumber
    - **YAML:** Metric definitions with versions
    """)
    
    st.warning("⚠️ Note: Document ingestion requires running `python ingest.py` after upload.")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload:",
        type=["pdf", "yaml", "yml"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.divider()
        st.subheader("📋 Files to Upload:")
        
        for file in uploaded_files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"✅ {file.name} ({file.size / 1024:.1f} KB)")
            with col2:
                file_type = "PDF" if file.name.endswith(".pdf") else "YAML"
                st.caption(file_type)
        
        if st.button("💾 Save to data/ folder", type="primary", use_container_width=True):
            data_dir = Path(__file__).parent / "data"
            docs_dir = data_dir / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            
            success_count = 0
            for file in uploaded_files:
                try:
                    if file.name.endswith(".pdf"):
                        save_path = docs_dir / file.name
                    else:  # yaml/yml
                        save_path = data_dir / file.name
                    
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                    success_count += 1
                except Exception as e:
                    st.error(f"Failed to save {file.name}: {e}")
            
            if success_count > 0:
                st.success(f"✅ Saved {success_count} file(s)")
                st.info("""
                **Next step:** Run this in your terminal:
                ```bash
                python ingest.py
                ```
                This will chunk, embed, and add all documents to the Chroma vector store.
                """)


# ============================================================================
# MODE 4: CHAT HISTORY
# ============================================================================
elif mode == "📋 Chat History":
    st.header("📋 Chat History")
    
    if not st.session_state.chat_history:
        st.info("No chat history yet. Start by asking a question in Chat mode!")
    else:
        st.write(f"**Total conversations:** {len(st.session_state.chat_history)}")
        st.divider()
        
        # Reverse order (most recent first)
        for idx, entry in enumerate(reversed(st.session_state.chat_history), 1):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            
            with st.expander(f"**{idx}.** {entry['question'][:60]}... — {timestamp}"):
                st.subheader("Question:")
                st.write(entry["question"])
                
                st.subheader("Answer:")
                st.markdown(f'<div class="answer-box">{entry["answer"]}</div>', unsafe_allow_html=True)
        
        # Export option
        st.divider()
        if st.button("💾 Export as JSON", use_container_width=True):
            json_str = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="Download chat history",
                data=json_str,
                file_name=f"rag_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


# ============================================================================
# Footer
# ============================================================================
st.divider()
st.markdown("""
---
**Investment RAG** | [GitHub](https://github.com/AdityaXplores/investment-rag)  
Built with ChromaDB · Streamlit · Local embeddings (all-MiniLM-L6-v2)
""", unsafe_allow_html=True)
