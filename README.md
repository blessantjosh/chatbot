# 📚 TNPSC Prep Copilot (Streamlit)

This project is a TNPSC-focused multilingual prep assistant built with Streamlit + OpenAI.
It is designed as a **single application** experience for:

- Syllabus guidance and study notes
- Previous-year question focus
- Model/mock paper generation
- Bilingual support (**Tamil + English**)
- Resource organization across mixed formats (files + links + pasted notes)

## What this app currently does

- Provides an interactive TNPSC assistant UI
- Lets you upload multiple resource files and add YouTube links
- Captures syllabus topics, exam group/stage, goals, and model paper needs
- Uses this context in a structured system prompt for LLM responses
- Supports chat-style planning, note generation, and mock-question generation

## Reality check on "zero errors"

No LLM can be guaranteed to return zero errors. A production-grade TNPSC assistant should combine:

1. Curated and versioned TNPSC source data
2. Retrieval pipeline (RAG) for grounded answers
3. Evaluation suite (Tamil + English)
4. Human review workflows
5. Monitoring + continuous improvement

This app is a strong **foundation/prototype** for that direction.

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start app:

```bash
streamlit run streamlit_app.py
```

3. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Suggested next implementation steps

- Add OCR + document parsing pipeline (PDF/DOCX/images/audio transcripts)
- Add vector database for semantic retrieval
- Add TNPSC-specific evaluation and benchmark dataset
- Add user login and progress tracking dashboard
- Add content moderation and factuality checks
