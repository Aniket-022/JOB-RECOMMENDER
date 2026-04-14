from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def compute_similarity(resume_text, job_list):
    """
    Compares the resume text against a list of job descriptions.
    Uses TF-IDF Vectorization and Cosine Similarity to score matches.
    Returns the jobs with an added 'match_score' & 'missing_skills'.
    """
    if not job_list:
        return []
        
    descriptions = []
    for job in job_list:
        # Combine title, skills, description for a comprehensive document matching base
        skills_str = " ".join(job.get('skills', []))
        desc = f"{job.get('title', '')} {skills_str} {job.get('description', '')}"
        
        # Clean special chars off description
        desc = re.sub(r'[^a-zA-Z0-9\+\s]', ' ', desc).lower()
        descriptions.append(desc)
    
    # Clean up the resume equally
    cleaned_resume = re.sub(r'[^a-zA-Z0-9\+\s]', ' ', resume_text).lower()
    
    # Document corpus: Index [0] is the resume, [1:] are jobs
    documents = [cleaned_resume] + descriptions
    
    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate Cosine Similarities (how closely [1:] match [0])
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    ranked_jobs = []
    # Set threshold of word matching (for skill gap analysis)
    resume_words = set(cleaned_resume.split())
    
    for idx, job in enumerate(job_list):
        # Scale score to percentage
        score = round(cosine_similarities[idx] * 100, 2)
        
        # Skill gap analysis loosely based on strings
        job_skills = set(s.lower() for s in job.get('skills', []))
        
        missing_skills = []
        for required_skill in job_skills:
            # simple single/multi word inclusion test against the clean resume
            if required_skill not in cleaned_resume:
                missing_skills.append(required_skill)
        
        # Copy job dict to avoid mutating original
        job_result = job.copy()
        job_result['match_score'] = score
        job_result['missing_skills'] = [ms.title() for ms in missing_skills]
        ranked_jobs.append(job_result)
        
    # Sort by match score descending
    ranked_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    return ranked_jobs
