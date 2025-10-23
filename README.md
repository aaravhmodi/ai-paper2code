# 🧬 AI Paper-to-Code Generator

A **Retrieval Augmented Generation (RAG)** system that converts AI research papers into runnable PyTorch code. Query your local vector database of research papers and get code implementations!

---

## 📋 Overview

This project:
1. **Scrapes** AI research papers from arXiv
2. **Embeds** paper abstracts into a ChromaDB vector database
3. **Retrieves** relevant papers based on semantic search
4. **Generates** PyTorch code using a large language model (Mistral-7B)

**Current Status:** ✅ **80 papers indexed** | ✅ **Vector DB populated** | 🚀 **Ready to use**

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │ "Implement diffusion model"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Streamlit Frontend (port 3000) │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   FastAPI Server (port 8000)    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   RAG Chain                     │
│   1. Retrieve (ChromaDB)        │
│   2. Generate (Mistral-7B)      │
└─────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Hugging Face Authentication

The generation model (Mistral-7B) requires authentication:

**Option A: Environment Variable**
```bash
# Windows PowerShell
$env:HF_TOKEN = "your_token_here"

# Windows CMD
set HF_TOKEN=your_token_here

# Linux/Mac
export HF_TOKEN=your_token_here
```

**Option B: CLI Login (Recommended)**
```bash
huggingface-cli login
```

Get your token from: https://huggingface.co/settings/tokens

### 3️⃣ Verify Database (Optional)

Check that your vector database has data:

```bash
python scripts/test_query.py
```

Expected: Returns 3 relevant papers about diffusion models.

### 4️⃣ Run the Application

**Terminal 1 - Start API Server:**
```bash
uvicorn src.server:app --reload
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run src/frontend.py
```

**Access:** Open http://localhost:8501 in your browser

---

## 📂 Project Structure

```
ai-paper2code/
├── data/
│   ├── metadata/
│   │   └── arxiv.json          # 80 paper metadata entries
│   └── papers/                  # PDF files (5 downloaded)
├── db/
│   └── chroma_db/              # Vector database (persistent)
├── src/
│   ├── arxiv_scraper.py        # Fetch papers from arXiv
│   ├── populate_chromadb.py    # Embed papers into database
│   ├── retriever.py            # Query vector database
│   ├── rag_chain.py            # RAG pipeline (retrieve + generate)
│   ├── server.py               # FastAPI backend
│   └── frontend.py             # Streamlit UI
├── scripts/
│   ├── test_query.py           # Test retrieval
│   ├── call_chain.py           # Test RAG chain
│   └── check_hf_access.py      # Verify HF authentication
└── requirements.txt
```

---

## 🔧 Usage Examples

### Via Web Interface

1. Open http://localhost:8501
2. Enter: `"Implement a transformer attention mechanism"`
3. Click "Generate Code"
4. Get PyTorch implementation!

### Via API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "implement CLIP training loop"}'
```

### Via Python Script

```python
from src.rag_chain import paper2code

result = paper2code.run("implement diffusion model")
print(result["answer"])
```

---

## 🔍 Available Scripts

| Script | Purpose |
|--------|---------|
| `python scripts/test_query.py` | Test vector database retrieval |
| `python scripts/call_chain.py` | Test full RAG pipeline |
| `python scripts/check_hf_access.py` | Verify HF token access |
| `python src/arxiv_scraper.py` | Fetch new papers from arXiv |
| `python src/populate_chromadb.py` | Re-populate vector database |

---

## 📊 Current Dataset

- **Papers:** 80 research papers
- **Topics:** Transformers, Diffusion Models, Graph Neural Networks, Language Models
- **Sources:** arXiv (cs.CV, cs.AI, cs.LG categories)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **LLM:** Mistral-7B-v0.1 (14GB download on first run)

---

## 🛠️ Customization

### Add More Papers

Edit search terms in `src/arxiv_scraper.py`:

```python
SEARCH_TERMS = ["transformer", "diffusion model", "your_topic_here"]
MAX_RESULTS = 50  # papers per query
```

Then run:
```bash
python src/arxiv_scraper.py
python src/populate_chromadb.py
```

### Change the LLM

Edit `src/rag_chain.py`:

```python
model_id = "mistralai/Mistral-7B-v0.1"  # Change this
# Options: codellama/CodeLlama-7b-hf, meta-llama/Llama-2-7b-chat-hf
```

### Adjust Retrieval

Edit `src/retriever.py`:

```python
def query_docs(query, n=5):  # Change n for more/fewer results
    ...
```

---

## ⚠️ Known Issues

1. **First Run Model Download:** Mistral-7B is ~14GB. First run will take time.
2. **GPU Required:** Generation is VERY slow on CPU (1-2 min per query).
3. **Windows Console:** May not display emojis correctly (cosmetic only).

---

## 🧪 Testing

### Quick Health Check
```bash
# 1. Test database
python scripts/test_query.py

# 2. Test API (server must be running)
python scripts/debug_request.py

# 3. Test RAG chain
python scripts/call_chain.py
```

---

## 📈 Roadmap (Future Enhancements)

- [ ] Fine-tune model on paper→code pairs (Phase 2)
- [ ] Add PDF full-text ingestion (currently only abstracts)
- [ ] Implement caching for faster responses
- [ ] Add code execution sandbox
- [ ] Multi-model support (OpenAI, Anthropic, etc.)
- [ ] Paper recommendation system

---

## 🤝 Contributing

This is a learning project! To add features:

1. Create a feature branch
2. Make your changes
3. Test with `scripts/test_*.py`
4. Submit a PR

---

## 📝 License

MIT License - Feel free to use for learning and projects!

---

## 🆘 Troubleshooting

### "HF_TOKEN not found"
Run `huggingface-cli login` or set the environment variable.

### "ChromaDB empty"
Run `python src/populate_chromadb.py` to populate the database.

### "Server connection refused"
Make sure FastAPI server is running: `uvicorn src.server:app --reload`

### "Generation is slow"
This is expected on CPU. Use a GPU or consider using API-based models (OpenAI/Anthropic).

### "ModuleNotFoundError"
Run `pip install -r requirements.txt` again.

---

## 📚 Learn More

- **RAG Architecture:** [LangChain RAG Docs](https://python.langchain.com/docs/use_cases/question_answering/)
- **ChromaDB:** [ChromaDB Documentation](https://docs.trychroma.com/)
- **Sentence Transformers:** [SBERT Documentation](https://www.sbert.net/)
- **Mistral AI:** [Mistral Models](https://mistral.ai/)

---

**Built with:** Python • ChromaDB • Sentence Transformers • FastAPI • Streamlit • Mistral-7B

**Status:** ✅ Fully Functional RAG Pipeline

