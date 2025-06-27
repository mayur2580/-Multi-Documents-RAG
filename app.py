import os
import textwrap
import re
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
from docx import Document as DocxReader
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

def read_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        st.warning(f"❌ Failed to read PDF {filepath}: {e}")
        return ""

def read_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.warning(f"❌ Failed to read TXT {filepath}: {e}")
        return ""

def read_docx(filepath):
    try:
        doc = DocxReader(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.warning(f"❌ Failed to read DOCX {filepath}: {e}")
        return ""

def split_into_chunks(text, max_words=100):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def highlight_keywords(answer, query):
    keywords = [word.lower() for word in query.split() if len(word) > 3]
    for word in keywords:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        answer = pattern.sub(f":blue[{word}]", answer)
    return answer

def read_and_chunk_documents(folder_path):
    chunks = []
    sources = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        text = ""
        if filename.endswith(".pdf"):
            text = read_pdf(filepath)
        elif filename.endswith(".txt"):
            text = read_txt(filepath)
        elif filename.endswith(".docx"):
            text = read_docx(filepath)
        if text.strip():
            doc_chunks = split_into_chunks(text)
            for chunk in doc_chunks:
                chunks.append(chunk)
                sources.append(filename)
    return chunks, sources

def main():
    st.title("📄 Multi - Doc RAG")
    folder_path = "documents"
    with st.spinner("Loading and encoding documents..."):
        all_chunks, source_map = read_and_chunk_documents(folder_path)
        if not all_chunks:
            st.error("No valid text found in documents.")
            return
        chunk_embeddings = model.encode(all_chunks, convert_to_tensor=True)

    query = st.text_input("🔎 Ask me Anything:")
    if query:
        query_embedding = model.encode(query, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
        top_k = 1
        top_indices = cosine_scores.argsort(descending=True)[:top_k]
        for rank, idx in enumerate(top_indices):
            score = cosine_scores[idx].item()
            if score < 0.3:
                st.info("No strong matches found.")
                continue
            highlighted = highlight_keywords(all_chunks[idx], query)
            st.markdown(f"**📄 Document:** {source_map[idx]}")
            st.markdown(f"**🔍 Similarity Score:** {score:.4f}")
            st.markdown("**📌 Answer:**")
            st.write(textwrap.fill(highlighted, width=100))

if __name__ == "__main__":
    main()