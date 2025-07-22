# Monopoly Rules RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers Monopoly rules questions using the official Monopoly rulebook as its knowledge base. The system uses a Python FastAPI backend with local embeddings and a simple HTML/CSS/JS frontend.

---

## Features
- **Ask any Monopoly rules question** and get an answer based on the official rulebook
- **Retrieval-Augmented Generation (RAG):**
  - Extracts and chunks the Monopoly rulebook PDF
  - Embeds the chunks using a sentence transformer
  - Retrieves the most relevant rules for each user question
  - Uses an LLM (via Ollama) to generate a concise, quoted answer
- **Simple web interface** (no frameworks required)

---

## Architecture
- **Frontend:** `index.html` (HTML/CSS/JS)
- **Backend:** `backend_api.py` (FastAPI) + `monopoly_chat.py` (RAG logic)
- **LLM:** Ollama running locally (e.g., Mistral)

---

## Setup

### 1. Prerequisites
- Python 3.8+
- Ollama installed and running locally (https://ollama.ai)
- MonopolyRulebook.pdf in the project directory

### 2. Install Python dependencies
```bash
pip install fastapi uvicorn sentence-transformers PyPDF2 numpy httpx
```

### 3. Start the backend
```bash
uvicorn backend_api:app --reload
```
- The backend will extract, chunk, and embed the rulebook on first run.
- The API will be available at http://localhost:8000/ask

### 4. Start Ollama and pull a model
```bash
ollama pull mistral
ollama serve
```

### 5. Open the frontend
- Open `index.html` in your browser (double-click or use a static server like `python3 -m http.server`).
- Ask any Monopoly rules question!

---

## Usage
- Type your question in the input box and click "Ask".
- The chatbot will retrieve relevant rules, send them to the LLM, and display a concise answer using the monopoly rulebook.

---

## Customization
- **Chunk size:** Adjust in `monopoly_chat.py` for more/less granular retrieval.
- **Model:** Change the model in `monopoly_chat.py` and in your Ollama setup.
- **Prompt:** Edit the prompt in `monopoly_chat.py` to change answer style.

---

## Future Improvements
- Add user chat history and context for multi-turn conversations
- Support for other board games (plug-and-play rulebooks)
- Use a vector database (e.g., FAISS, ChromaDB) for faster and more scalable retrieval
- Add admin interface for uploading new rulebooks or custom house rules
- Improve PDF parsing and rule chunking for even better accuracy
- Add authentication and user profiles
- Deploy backend and frontend to the cloud for public access
- Add mobile-friendly UI and dark mode
- Support for voice input/output
