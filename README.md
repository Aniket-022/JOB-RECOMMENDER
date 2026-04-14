# AI-Powered Job Recommendation System (Hybrid Model)

## 🎯 Project Overview
This Streamlit-based web application recommends jobs and internships by matching your resume against a hybrid data source using Natural Language Processing (NLP).

It automatically parses your resume (PDF), extracts technical skills, and matches you against job descriptions using **TF-IDF mapping** and **Cosine Similarity**. It even highlights skill gaps to help you improve!

## ✨ Features
1. **Resume Analysis**: Uses `pdfplumber` and `spaCy` to digest PDF resumes and identify key skills.
2. **Hybrid Data Source**: Pulls from a local curated dataset (`jobs.json`) AND acts as a conduit for live Job APIs (like JSearch via RapidAPI, with built-in mock fallbacks).
3. **Core Matching Engine**: Uses `scikit-learn` to vectorize text and rank jobs by similarity percentage.
4. **Skill Gap Analyzer**: Highlights which skills you're missing for a specific listing.
5. **Bonus Functionalities**: Downloads results as CSV, identifies top skills in demand in the sidebar, and calculates your resume's overall parsed score.

## 🚀 Step-by-Step Setup Instructions

**1. Clone or Download the repository.**
Ensure your terminal is in the `job-recommender/` directory.

**2. Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run Spacy Model Download**
(The app attempts to download this automatically, but you can do it manually):
```bash
python -m spacy download en_core_web_sm
```

**5. Start the Application**
```bash
streamlit run app.py
```

## 📂 Project Structure
- `app.py`: Streamlit frontend UI and main application flow.
- `parser.py`: PDF extraction and spaCy-powered NLP skill tagging.
- `matcher.py`: TF-IDF Vectorization and Cosine Similarity computations.
- `api_fetcher.py`: Live integration logic for fetching dynamic jobs (with fallback).
- `utils.py`: Helper functions for JSON ingestion and filtering.
- `data/jobs.json`: Sample dataset of ~20 job entries.
- `requirements.txt`: Python package dependencies.
