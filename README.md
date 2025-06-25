# 🎥 YouTube RAG + Flashcard Generator App

This app lets you analyze YouTube lectures using LLMs, automatically summarize their content, and generate flashcards on any topic from the video. It's designed for researchers, students, and AI enthusiasts who want to quickly digest technical videos using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

```
- ✅ Paste one or more YouTube links
- 🧠 GPT-4 powered **summaries** with:
  - Key Topics
  - Definitions
  - Key Points
  - Examples
- 🔍 Ask topic-specific questions and generate flashcards in `Q:` / `A:` format
- 🧭 FAISS vector index for fast semantic search
- 🪂 Fallback flashcards for unmatched queries
- 🎯 Streamlit UI for smooth interactivity
```

# 📦 Project Structure

```
📁 youtube-rag-flashcards/
│
├── app.py                    # Streamlit frontend
├── config.yaml               # API keys & settings
├── requirements.txt          # Python dependencies
├── utils/                    # Modular utility functions
│   ├── youtube\_utils.py     # YouTube transcript/title extraction
│   ├── chunking.py           # Chunk long text for RAG
│   ├── embeddings.py         # OpenAI embeddings & FAISS
│   ├── retrieval.py          # Vector search logic
│   ├── summarization.py      # Prompted GPT-4 summaries
│   ├── flashcards.py         # Topic-driven or fallback flashcards
│   └── storage.py            # Save/load FAISS (optional)
```

---

## 🛠️ Installation

```bash
git clone https://github.com/shubbham28/Youtube_rag.git
cd youtube_rag
# Optional: create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
# Install dependencies
pip install -r requirements.txt
# Run the app
streamlit run app.py
````

---

## ⚙️ Configuration

Create a `config.yaml` file in the root directory:

```yaml
openai_api_key: "sk-..."  # or use dotenv and "env:OPENAI_API_KEY"
embedding_model: "openai"
chunk_size: 500
chunk_overlap: 100
```

> You can use `env:` for secrets, or hardcode them locally while testing.

---

## 📄 Example Workflow

1. Paste one or more YouTube links (e.g., ML lectures)
2. The app fetches the transcript and splits it into semantic chunks
3. GPT-4 summarizes each lecture under sections like:

   * **Key Topics**
   * **Definitions**
   * **Key Points**
   * **Examples**
4. User enters a topic (e.g., "transformers") and gets:

   * Q/A formatted flashcards if found in transcript
   * Fallback general flashcards if not

---

## 📚 Dependencies

Install via `requirements.txt`. Key packages:

* `streamlit`
* `openai`
* `faiss-cpu`
* `youtube-transcript-api`
* `yt-dlp`
* `pyyaml`
* `tqdm`

---

## 💡 Use Cases

* Convert long videos into readable summaries
* Generate topic-specific revision notes
* Build educational apps or agents using this as backend

---

## 🧠 Tech Stack

| Component  | Library                       |
| ---------- | ----------------------------- |
| LLMs       | OpenAI GPT-3.5                  |
| Embeddings | OpenAI + FAISS                |
| UI         | Streamlit                     |
| Retrieval  | Custom + FAISS                |
| Transcript | YouTube Transcript API        |

---

## 📝 License

MIT License © 2025 \Shubbham Gupta

---

## 📬 Contact

Made with ❤️ by Shubbham Gupta
For feedback, feel free to open an issue or reach out.

```
