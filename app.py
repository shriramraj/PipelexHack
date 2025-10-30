import os
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Customer Support Responder", page_icon="💬")

st.title("💬 AI Customer Support Responder")

# --- Sidebar: upload or link FAQ data ---
st.sidebar.header("FAQ Source")
use_url = st.sidebar.toggle("Use CSV from URL", value=False)

faq_df = None
if use_url:
    csv_url = st.sidebar.text_input("Public CSV URL (columns: category,question,answer)")
    if csv_url:
        try:
            faq_df = pd.read_csv(csv_url)
        except Exception as e:
            st.sidebar.error(f"Failed to load CSV from URL: {e}")
else:
    uploaded = st.sidebar.file_uploader("Upload CSV (category,question,answer)", type=["csv"])
    if uploaded:
        try:
            faq_df = pd.read_csv(uploaded)
        except Exception as e:
            st.sidebar.error(f"Failed to parse CSV: {e}")

# --- Validate and preview data ---
if faq_df is None:
    st.info("👆 Upload or link a CSV file with columns: category, question, answer.")
    st.stop()

faq_df = faq_df.rename(columns=str.lower)
required_cols = {"question", "answer"}
if not required_cols.issubset(set(faq_df.columns)):
    st.error(f"CSV must include columns: {required_cols}. Found: {list(faq_df.columns)}")
    st.stop()

with st.expander("Preview FAQ data"):
    st.dataframe(faq_df.head(20), use_container_width=True)

# --- Build a simple TF-IDF retriever ---
faq_df["blob"] = faq_df["question"].astype(str) + " || " + faq_df["answer"].astype(str)
texts = faq_df["blob"].tolist()
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
X = vectorizer.fit_transform(texts)

def retrieve_context(query, k=5, max_chars=1500):
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, X).flatten()
    idxs = sims.argsort()[::-1][:k]
    rows = faq_df.iloc[idxs]
    context_items = []
    for _, r in rows.iterrows():
        cat = r.get("category", "")
        context_items.append(f"- [Cat: {cat}] Q: {r['question']}\n  A: {r['answer']}")
    return "\n".join(context_items)[:max_chars]

# --- Local retrieval fallback (no API) ---
def run_pipelex_support(question, context):
    """Returns the first FAQ answer from retrieved context."""
    lines = context.splitlines()
    for line in lines:
        if "A:" in line:
            return line.replace("A:", "").strip()
    return "I don’t have that information yet, but a human can help."

# --- Streamlit chat interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_input = st.chat_input("Ask a support question…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        ctx = retrieve_context(user_input, k=5)
        with st.spinner("Thinking…"):
            answer = run_pipelex_support(user_input, ctx)
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})