# Multi-Documents-RAG
Multi-Documents-RAG is a lightweight Retrieval-Augmented Generation (RAG) system built using Streamlit, SentenceTransformers, and various NLP tools to intelligently answer user queries by retrieving information from multiple document formats (PDF, DOCX, and TXT). It uses embedding-based search to identify relevant chunks of text and highlights relevant keywords.

# 🚀 Features
📂 Supports .pdf, .docx, and .txt document types

🧠 Embedding-based semantic search using multi-qa-MiniLM-L6-cos-v1

🧵 Splits documents into manageable chunks for accurate retrieval

🔍 Accepts user queries and returns the most relevant document snippets

🎨 Highlights keywords in results for easy scanning

💡 Easy-to-use Streamlit interface

# 📁 Project Structure
bash
Copy
Edit
├── app.py                # Main Streamlit application
├── requirements.txt      # Required Python packages
├── .env                  # Contains API keys (not to be shared)
├── documents/            # Folder to store all PDF, DOCX, and TXT files

# 🛠️ Installation
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/Multi-Documents-RAG.git
cd Multi-Documents-RAG
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Add your OpenAI API Key
Create a .env file in the root directory:

bash
Copy
Edit
OPENAI_API_KEY=your_openai_api_key

# ▶️ Run the App
bash
Copy
Edit
streamlit run app.py

# 🧪 Example Use Case
Upload multiple documents to the documents/ folder.

Run the Streamlit app.

Ask natural language questions like:

"What is the summary of the agreement in contract.pdf?"

The app will retrieve the most relevant section and highlight key terms.

# 📌 Notes
Currently retrieves only the top match (top_k = 1) based on cosine similarity.

Matching threshold is set to 0.3 — results below this score are ignored.

You can adjust max_words, top_k, or the model as needed.

# 🔐 Security
⚠️ Never share your .env file publicly — it contains sensitive API keys. Be sure to include .env in your .gitignore.

