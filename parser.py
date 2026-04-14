import pdfplumber
import spacy
import re

# Safely load the NLP model, natively downloading it via the spacy Python API if missing
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file_path_or_bytes):
    """
    Extracts purely textual content from a PDF file
    """
    text = ""
    with pdfplumber.open(pdf_file_path_or_bytes) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_and_extract_skills(text):
    """
    Cleans the resume text and extracts identifiable technical/soft skills
    using a hybrid of predefined skills dictionary and Spacy tokenization.
    """
    # Basic cleaning
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\+]', ' ', text) # keeping + for c++
    
    # Process text with spacy
    doc = nlp(text)
    
    # Pre-defined repository of common skills
    KNOWN_SKILLS = {
        "python", "java", "c++", "c#", "javascript", "typescript", "react", "angular", "vue",
        "node", "sql", "nosql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp",
        "docker", "kubernetes", "machine learning", "deep learning", "nlp", "html", "css",
        "excel", "powerbi", "tableau", "statistics", "mathematics", "git", "bash", "linux",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "django", "flask",
        "fastapi", "spring boot", "ruby", "php", "swift", "kotlin", "go", "rust",
        "data analysis", "data engineering", "devops", "agile", "scrum", "ui", "ux",
        "problem solving", "communication", "leadership", "time management", "teamwork", "jira",
        "figma", "testing", "selenium", "spark", "hadoop", "architecture", "api design"
    }
    
    # We will track found skills
    extracted_skills = set()
    
    # 1. Multi-word phrase matching
    for skill in KNOWN_SKILLS:
        if " " in skill and skill in text:
            extracted_skills.add(skill)
            
    # 2. Token-level matching
    for token in doc:
        word = token.lemma_.lower()
        if word in KNOWN_SKILLS:
            extracted_skills.add(word)
            
        # Also check exact text incase lemma fails
        if token.text in KNOWN_SKILLS:
            extracted_skills.add(token.text)
            
    return list(extracted_skills), text
