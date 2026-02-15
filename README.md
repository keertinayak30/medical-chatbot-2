---
title: Medical Chatbot
emoji: 👩🏻‍⚕️
colorFrom: green
colorTo: green
sdk: docker
python_version: "3.10"
app_file: app.py
pinned: false
---
# MediBot AI: Medical Assistant Chatbot

**Live Demo:** [Click here to launch the Chatbot](https://keertinayak30-medical-chatbot.hf.space/)

## Overview
Built a Retrieval-Augmented Generation (RAG) medical chatbot using the Gale Encyclopedia of Medicine.

## Tech Stack
* **Framework:** Flask (Python)
* **LLM Orchestration:** LangChain
* **Large Language Model:** Llama-3.3-70b (via Groq Cloud)
* **Vector Database:** Pinecone
* **Embeddings:** Hugging Face `all-MiniLM-L6-v2`
* **Deployment:** Docker & Hugging Face Spaces

## Features
* **Conversational Memory:** Remembers the context of the current conversation for more natural interactions.
* **Source-Grounded Answers:** Uses a dedicated medical knowledge base to minimize hallucinations.
* **Fast Inference:** Powered by the Groq LPU™ Inference Engine for near-instant responses.
* **Professional UI:** A clean, dark-mode-ready interface for an intuitive user experience.

## How it Works
1. **Data Ingestion:** Medical PDFs are split into chunks and converted into vector embeddings.
2. **Vector Search:** User queries are embedded and compared against the Pinecone index to find relevant medical context.
3. **RAG Chain:** The retrieved context and the user's question are sent to the Llama model to generate a grounded response.

## 📁 Project Structure
* `app.py`: Main Flask application and API routes.
* `src/helper.py`: Utility functions for embeddings and data processing.
* `src/prompt.py`: System prompts and logic for the AI's behavior.
* `templates/`: HTML frontend files.
* `static/`: CSS and JavaScript assets.

*Disclaimer: This chatbot is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.*
