# Confluence RAG (Retrieval-Augmented Generation)

A lightweight RAG system that fetches Confluence pages, creates embeddings, and performs semantic search using OpenAI's embedding models.

## 🎯 Features

- **Fetch Confluence Pages** - Retrieve pages from Confluence Cloud using CQL queries
- **Create Embeddings** - Convert text chunks into vector embeddings (OpenAI text-embedding-3-small)
- **Semantic Search** - Find relevant pages using cosine similarity
- **Vector Store** - Persist embeddings as pickle files for fast retrieval

## 📁 Project Structure

```
confluence_embedding_poc/
├── fetch_confluence.py      # Fetch pages from Confluence
├── embed_pages.py           # Create embeddings & chunk text
├── search.py                # Semantic search functionality
├── requirements.txt         # Python dependencies
└── confluence_vectordb.pkl  # Stored embeddings
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file:
```
CONFLUENCE_API_KEY=your_confluence_api_token
OPENAI_API_KEY=your_openai_api_key
```

### 3. Fetch & Embed Pages
```bash
cd confluence_embedding_poc
python embed_pages.py  # Fetches pages and creates embeddings
```

### 4. Search Pages
```bash
python search.py  # Interactive search
```

## 📚 How It Works

### 1. Fetch Confluence Pages
```python
from fetch_confluence import fetch_pages

# Get pages from your Confluence space
pages = fetch_pages(space_key="your_space_key")
```

### 2. Create Embeddings
- Chunks text into 500-character segments with 100-character overlap
- Generates OpenAI embeddings for each chunk
- Stores embeddings in `confluence_vectordb.pkl`

### 3. Semantic Search
- Embeds your query
- Calculates cosine similarity against all stored embeddings
- Returns most relevant pages

## 🔧 Key Functions

### `fetch_pages(space_key, limit=50)`
Fetches pages from a Confluence space using CQL query.

### `chunk_text(text, chunk_size=500, overlap=100)`
Splits text into overlapping chunks for better embedding coverage.

### `cosine_sim(a, b)`
Calculates cosine similarity between two vectors:
```
similarity = A · B / (|A| × |B|)
```

## 🛠️ Dependencies

- `atlassian-python-api` - Confluence API client
- `openai` - OpenAI embeddings
- `numpy` - Vector operations
- `python-dotenv` - Environment variables

## 📝 Environment Variables

```bash
CONFLUENCE_API_KEY=your_api_token        # Confluence Cloud API token
OPENAI_API_KEY=your_openai_key           # OpenAI API key
```

Get your Confluence API token from: https://id.atlassian.com/manage-profile/security/api-tokens

## ⚙️ Configuration

Edit these constants in the source files:

- `EMBEDDING_MODEL` - OpenAI model (default: `text-embedding-3-small`)
- `CHUNK_SIZE` - Text chunk size (default: 500)
- `OVERLAP` - Chunk overlap (default: 100)

## 🔍 Example Usage

```python
from search import embedding_query

# Search for relevant pages
results = embedding_query("What is your company policy on remote work?")
# Returns top matching pages with similarity scores
```

## 🐛 Troubleshooting

**Auth Error on Confluence Fetch:**
- Verify API token in `.env`
- Check token hasn't expired
- Confirm space key is correct

**OpenAI API Error:**
- Check `OPENAI_API_KEY` is set correctly
- Verify API key has embeddings permission

**No Results Found:**
- Ensure embeddings are created: `python embed_pages.py`
- Check `confluence_vectordb.pkl` exists
- Try broader search terms

## 📊 Tech Stack

- **Python 3.8+**
- **OpenAI API** - Embeddings generation
- **Confluence Cloud API** - Page retrieval
- **NumPy** - Vector math
- **Pickle** - Serialization

## 📖 Learn More

- [Confluence API Docs](https://developer.atlassian.com/cloud/confluence/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Cosine Similarity Formula](https://en.wikipedia.org/wiki/Cosine_similarity)

## 📄 License

MIT

---

**Built with ❤️ for semantic search on Confluence**
