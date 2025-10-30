🧩 AI Customer Support Responder

A lightweight Streamlit-based AI SaaS prototype that transforms any FAQ dataset (CSV or URL) into an interactive customer support chatbot — no API keys required.
Built for the Pipelex × BlackboxAI Hackathon, this demo showcases how structured FAQs can power intelligent, context-aware question answering.

⸻

🚀 Features
	•	📄 Upload or link a CSV file (category, question, answer)
	•	💬 Ask natural-language questions like “Do you offer international shipping?”
	•	🔍 TF-IDF retrieval engine to match semantically similar questions
	•	⚙️ Offline-friendly — works with or without API keys
	•	🧠 Optional Pipelex/LLM integration (future-ready)
	•	📊 Built with Streamlit, pandas, and scikit-learn

⸻

🧠 Demo Ideas
	•	Replace CSVs to simulate domain-specific helpdesks (e.g., Tech Support, eCommerce, Product Docs)
	•	Connect Pipelex or OpenAI backend for live inference
	•	Deploy easily via Streamlit Cloud or Hugging Face Spaces

⸻

🏗️ Setup
git clone https://github.com/<your-username>/ai-support-bot.git
cd ai-support-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

🧩 Future Enhancements
	•	Confidence scoring for each answer
	•	Multi-CSV knowledge base merging
	•	Chat memory and user feedback analytics
	•	Cloud deployment with telemetry and real-time logs

⸻

🏷️ Tags

#AI #Streamlit #Hackathon #Pipelex #CustomerSupport #FAQBot #BlackboxAI
