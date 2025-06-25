# app.py

import streamlit as st
import yaml
from utils.youtube_utils import extract_video_id, fetch_transcript,fetch_video_title
from utils.chunking import chunk_text
from utils.embeddings import embed_chunks_openai, build_faiss_index
from utils.retrieval import query_topic
from utils.flashcards import generate_flashcards, fallback_flashcards
from utils.summarization import generate_video_summary
from utils.storage import save_faiss_to_hf

import numpy as np
import os
from tempfile import NamedTemporaryFile
from huggingface_hub import hf_hub_download
import faiss
import re

from openai import OpenAI


# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(api_key=config["openai_api_key"])

st.set_page_config(page_title="YouTube RAG Flashcard App", layout="wide")
st.title("🎓 YouTube Lecture Analyzer with Flashcards")

# Step 1: Upload YouTube links
youtube_input = st.text_area("Paste one or more YouTube links (one per line):")

if st.button("📥 Process Videos"):
    if not youtube_input.strip():
        st.warning("Please paste at least one YouTube URL.")
    else:
        links = youtube_input.strip().splitlines()
        st.session_state.chunks = []
        st.session_state.summaries = []
        all_chunks = []
        video_ids = []

        with st.spinner("Fetching transcripts and chunking..."):
            for url in links:
                vid = extract_video_id(url)
                if vid:
                    try:
                        text = fetch_transcript(vid)
                        chunks = chunk_text(
                            text,
                            chunk_size=config["chunk_size"],
                            overlap=config["chunk_overlap"]
                        )
                        summary = generate_video_summary(chunks, client)
                        video_ids.append(vid)
                        all_chunks.extend(chunks)
                        title = fetch_video_title(vid)
                        st.session_state.summaries.append((title, summary))
                    except Exception as e:
                        st.error(f"Failed for {url}: {str(e)}")

        # Step 2: Embed and build FAISS
        with st.spinner("Embedding and indexing all transcripts..."):
            embeddings = embed_chunks_openai(all_chunks, client)
            index = build_faiss_index(embeddings)

        # Step 3: Save FAISS index
        st.session_state.index = index
        st.session_state.all_chunks = all_chunks
        st.success("Vector index built and saved.")
#         faiss_path = config["faiss_save_path"]
#         os.makedirs(os.path.dirname(faiss_path), exist_ok=True)
#         with NamedTemporaryFile(delete=False, suffix=".index") as tmp:
#             save_faiss_to_hf(index, tmp.name, config["hf_repo_id"], os.path.basename(faiss_path))


# Step 4: Show summaries
if "summaries" in st.session_state:
    st.subheader("📄 Video Summaries")
    for title, summary in st.session_state.summaries:
        with st.expander(f"Summary for: {title}"):
            st.markdown(summary)

# Step 5: Flashcards below summaries
if "summaries" in st.session_state and "index" in st.session_state:
    st.divider()
    st.subheader("🧠 Generate Flashcards by Topic")

    # Track previous topic to clear stale output
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = None
    if "cards_output" not in st.session_state:
        st.session_state.cards_output = ""

    user_topic = st.text_input("Enter a topic you'd like flashcards on:")

    if user_topic and user_topic != st.session_state.last_topic:
        st.session_state.last_topic = user_topic

        top_chunks = query_topic(
            topic=user_topic,
            index=st.session_state.index,
            chunks=st.session_state.all_chunks,
            client=client,
            threshold=0.99
        )

        if top_chunks:
            st.success("✅ Topic found. Generating flashcards...")
            st.session_state.cards_output = generate_flashcards(top_chunks, client)
        else:
            st.warning("⚠️ Topic not found. Generating general flashcards...")
            st.session_state.cards_output = fallback_flashcards(user_topic, client)

    if st.session_state.cards_output:
        st.markdown("### 📚 Flashcards")
        st.code(st.session_state.cards_output, language="markdown")

