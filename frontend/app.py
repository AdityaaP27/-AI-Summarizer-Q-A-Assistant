import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE")

# --- Page Config & Global CSS ---
st.set_page_config(page_title="AI Summarizer & Q&A", layout="wide")

st.markdown("""
    <style>
    .summary-container, .keypoints-container, .qa-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 16px;
        color: #333333;
    }
    .btn-index {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .btn-index:hover { background-color: #45a049; }
    .btn-ask {
        background-color: #2196F3;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        cursor: pointer;
    }
    .btn-ask:hover { background-color: #1e88e5; }
    </style>
""", unsafe_allow_html=True)

# --- Title & Instructions ---
st.title("🌐 AI Summarizer & Q&A Assistant")
st.markdown("""
Enter a **URL**, get a concise **summary** and **key points**, then **index** the content to ask **questions** interactively.
""")

# --- URL Input & Summarization ---
url = st.text_input("🔗 Enter article URL", placeholder="https://example.com/article")

if st.button("📄 Summarize"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Fetching and summarizing…"):
            try:
                resp = requests.post(f"{API_BASE}/summarize", json={"url": url}, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                st.session_state.summary = data["summary"]
                st.session_state.key_points = [pt.strip() for pt in data["key_points"] if pt.strip()]
                st.session_state.indexed = False  # reset Q&A state
            except Exception as e:
                st.error(f"Summarization failed: {e}")

# --- Display Results ---
if st.session_state.get("summary"):
    # Summary Section
    st.markdown("### ✍️ Summary")
    st.markdown(f'<div class="summary-container">{st.session_state.summary}</div>', unsafe_allow_html=True)

    # Key Points Section
    st.markdown("### 🗝️ Key Points")
    key_points = st.session_state.key_points
    if key_points:
        num_points = len(key_points)
        num_cols = min(3, num_points)  # max 3 columns
        cols = st.columns(num_cols)

        for idx, point in enumerate(key_points):
            cols[idx % num_cols].markdown(f"🔹 {point}")
    else:
        st.info("No key points available.")

    # Index for Q&A Button
    if not st.session_state.get("indexed"):
        if st.button("🧠 Index for Q&A"):
            with st.spinner("Indexing content…"):
                try:
                    idx_resp = requests.post(f"{API_BASE}/index", json={"url": url}, timeout=120)
                    idx_resp.raise_for_status()
                    st.success("✅ Content indexed! You can now ask questions.")
                    st.session_state.indexed = True
                except Exception as e:
                    st.error(f"Indexing failed: {e}")

# --- Q&A Section ---
if st.session_state.get("indexed"):
    st.markdown("### ❓ Ask a Question")
    question = st.text_input("Your question about the content", key="qa_input")
    ask_col1, ask_col2, _ = st.columns([3, 1, 2])
    with ask_col2:
        if st.button("Ask", key="ask_btn"):
            if not question.strip():
                st.warning("Please type a question.")
            else:
                with st.spinner("Generating answer…"):
                    try:
                        qa_resp = requests.post(f"{API_BASE}/query", json={"question": question}, timeout=60)
                        qa_resp.raise_for_status()
                        qa_data = qa_resp.json()
                        st.markdown("### 💬 Answer")
                        st.markdown(f'<div class="qa-container">{qa_data["answer"]}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Q&A error: {e}")
