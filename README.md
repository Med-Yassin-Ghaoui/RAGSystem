# 🔍 RAGSystem

A full-stack **Retrieval-Augmented Generation (RAG)** pipeline that lets you chat with your documents. Upload PDFs or text files, and get accurate, context-grounded answers powered by **Google Gemini**, with semantic search backed by **Qdrant** and async orchestration via **Inngest**.

---

## ✨ Features

- 📄 **Document ingestion** — Upload PDFs and plain text files for processing
- 🧩 **Chunking & embedding** — Documents are split and embedded for semantic retrieval
- 🗄️ **Vector storage** — Embeddings are stored and queried via Qdrant
- 🤖 **Gemini-powered generation** — Retrieved context is fed to Google Gemini for grounded answers
- ⚙️ **Inngest orchestration** — Async, event-driven workflows for ingestion and indexing pipelines
- 🖥️ **Streamlit UI** — Clean, interactive interface for uploading documents and asking questions

---

## 🏗️ Architecture

```
User (Streamlit UI)
      │
      ├─── Upload document ──► Inngest Workflow
      │                              │
      │                    Chunk ──► Embed ──► Qdrant (store vectors)
      │
      └─── Ask question ──► Embed query ──► Qdrant (retrieve top-k chunks)
                                                    │
                                           Gemini API (generate answer)
                                                    │
                                           Answer displayed in UI
```

---

## 🛠️ Tech Stack

| Component        | Technology              |
|------------------|-------------------------|
| LLM              | Google Gemini API       |
| Vector Database  | Qdrant                  |
| Orchestration    | Inngest                 |
| UI               | Streamlit               |
| Language         | Python                  |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A running [Qdrant](https://qdrant.tech/documentation/quick-start/) instance (local or cloud)
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- An [Inngest](https://www.inngest.com/) account (or local dev server)

### Installation

```bash
git clone https://github.com/Med-Yassin-Ghaoui/RAGSystem.git
cd RAGSystem
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the root of the project:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Running the App

**1. Start the Inngest dev server** (for local orchestration):
```bash
npx inngest-cli@latest dev
```

**2. Launch the Streamlit app:**
```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
RAGSystem/
├── app.py                  # Streamlit UI entrypoint
├── ingestion/
│   ├── chunker.py          # Document splitting logic
│   ├── embedder.py         # Embedding generation
│   └── inngest_functions.py# Inngest workflow definitions
├── retrieval/
│   ├── qdrant_client.py    # Qdrant vector store interface
│   └── retriever.py        # Top-k similarity search
├── generation/
│   └── gemini.py           # Gemini API calls & prompt construction
├── utils/
│   └── file_parser.py      # PDF / text file parsing
├── .env.example
├── requirements.txt
└── README.md
```

> ⚠️ Structure may vary — update this section to match your actual layout.

---

## 📸 Demo

> _Add a screenshot or GIF of the Streamlit interface here._

---

## 🔧 Roadmap

- [ ] Multi-document session support
- [ ] Metadata filtering in retrieval
- [ ] Streaming responses from Gemini
- [ ] Conversation memory / chat history
- [ ] Docker Compose setup for one-command deployment

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

## 👤 Author

**Med Yassin Ghaoui**
- GitHub: [@Med-Yassin-Ghaoui](https://github.com/Med-Yassin-Ghaoui)
