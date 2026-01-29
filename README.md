# RAG Agent - Capstone Project

A simple RAG (Retrieval Augmented Generation) system that generates summaries and sends notifications.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install and start Ollama:
```bash
ollama pull llama2
```

3. Copy `.env.example` to `.env` and add your credentials.

4. Run:
```bash
python main.py
```

## How It Works

1. Loads text documents from `data/sample_documents/`
2. Creates embeddings using Sentence Transformers
3. Stores vectors in FAISS database
4. Retrieves relevant chunks based on query
5. Generates summary using Ollama LLM
6. Saves to SQLite and sends notifications

## Project Structure

```
├── main.py              # Entry point
├── config/
│   └── settings.py      # Configuration


├── modules/
│   ├── embeddings.py    # Sentence Transformer embeddings
│   ├── vector_db.py     # FAISS vector database
│   ├── llm_client.py    # Ollama LLM client
│   ├── database.py      # SQLite storage
│   └── rag_pipeline.py  # Main RAG logic
├── services/
│   ├── whatsapp_service.py
│   ├── sms_service.py
│   └── email_service.py
└── data/
    └── sample_documents/
```

## Requirements

- Python 3.10+
- Ollama (for local LLM)
- Twilio account (for WhatsApp/SMS)
- Gmail account (for email)
