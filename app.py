import streamlit as st
import os
import pandas as pd
from parser import extract_text_from_pdf, clean_and_extract_skills
from matcher import compute_similarity
from api_fetcher import fetch_jobs_from_api
from utils import load_local_jobs, filter_jobs

# Set page config
st.set_page_config(
    page_title="Job Recommender",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI improvement
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6; 
    border-radius: 10px; 
    padding: 10px; 
    text-align: center;
}
.skill-pill {
    display: inline-block;
    background-color: #4CAF50;
    color: white;
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 14px;
    margin: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("💼 AI-Powered Job Recommendation System")
st.markdown("Upload your resume, set your preferences, and let AI find and rank the best jobs (Internships & Full-time) for you!")

# Sidebar preferences
st.sidebar.header("⚙️ User Preferences")
user_name = st.sidebar.text_input("Name (Optional)", placeholder="e.g. John Doe")
user_age = st.sidebar.number_input("Age (Optional)", min_value=18, max_value=100, value=22)
pref_location = st.sidebar.text_input("Preferred Location", value="", placeholder="e.g. Bangalore, Remote")
job_type = st.sidebar.selectbox("Job Type", ["Internship", "Full-time", "Contract"])

st.sidebar.markdown("---")
st.sidebar.markdown("### API Integration")
api_key = st.sidebar.text_input("JSearch API Key (Optional)", type="password", help="Leave blank to use Hybrid Mock API jobs + Local Dataset")

# Main interface
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF format)", type=["pdf"])

if uploaded_file is not None:
    # 1. Parse Resume
    with st.spinner("Extracting and analyzing text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        skills, cleaned_text = clean_and_extract_skills(resume_text)
    
    st.success("Resume parsed successfully!")
    
    # Display Score Profile (ATS style)
    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Total Words Parsed", value=len(resume_text.split()))
    with colB:
        st.metric(label="Skills Identified", value=len(skills))
        
    with st.expander("🛠️ View Identified Skills"):
        if skills:
            skills_html = "".join([f"<span class='skill-pill'>{s.title()}</span>" for s in skills])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No common tech skills detected. Make sure your resume is text-based and not a scanned image.")

    st.markdown("---")
    
    # 2. Action to fetch jobs
    if st.button("🚀 Find Matching Jobs", type="primary"):
        with st.spinner("Fetching and ranking jobs based on your profile..."):
            
            # Step A: Load Local Jobs
            local_jobs = load_local_jobs()
            
            # Step B: Fetch API Jobs
            api_jobs = fetch_jobs_from_api(pref_location, job_type, api_key)
            
            # Combine them
            all_jobs = local_jobs + api_jobs
            
            # Step C: Filter based on preferences
            filtered_jobs = filter_jobs(all_jobs, pref_location, job_type)
            
            if not filtered_jobs:
                st.warning("No jobs matching your specific Location and Type preferences. Evaluating all available data instead...")
                filtered_jobs = all_jobs
                
            # Step D: Rank Jobs via TF-IDF Cosine Similarity
            ranked_jobs = compute_similarity(resume_text, filtered_jobs)
            
            st.subheader(f"Top Job Recommendations for {user_name if user_name else 'You'}")
            
            if not ranked_jobs:
                st.error("No valid jobs to analyze.")
            else:
                # Top Demanded Skills Analysis
                st.sidebar.markdown("---")
                st.sidebar.markdown("### 📈 Top Skills in Demand")
                all_demanded = []
                for j in ranked_jobs[:10]:
                    all_demanded.extend(j.get('skills', []))
                
                if all_demanded:
                    skill_counts = pd.Series([s.title() for s in all_demanded]).value_counts().head(5)
                    for sk, count in skill_counts.items():
                        st.sidebar.markdown(f"- **{sk}** ({count} jobs)")
                
                # Display individual ranked cards
                for job in ranked_jobs[:10]: # Return Top 10
                    st.divider()
                    col1, col2 = st.columns([4, 1])
                    
                    score = job['match_score']
                    
                    with col1:
                        st.markdown(f"### {job['title']}")
                        st.write(f"📍 **{job['location']}** | 💼 **{job['type']}**")
                        
                        req_skills = job.get('skills', [])
                        if req_skills:
                            st.markdown(f"*Required Skills*: {', '.join(req_skills)}")
                        
                        missing = job.get('missing_skills', [])
                        if missing:
                            st.warning(f"**Skill Gap (Missing)**: {', '.join(missing)}")
                        else:
                            st.success("**Great fit!** No obvious skill gaps detected.")
                            
                        with st.expander("📝 Read Full Description"):
                            st.write(job.get('description', 'No description provided.'))
                            
                    with col2:
                        # Dynamic color for match percentage
                        color = "green" if score >= 60 else "orange" if score >= 30 else "red"
                        st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                        st.markdown(f"<h2 style='color: {color}; margin: 0;'>{score}%</h2>", unsafe_allow_html=True)
                        st.markdown("<p style='margin: 0; color: gray;'>Match</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Add a fake 'Save Job' button for UI points
                        st.button("⭐ Save", key=job['title']+str(score))
                        
                st.markdown("---")
                
                # Bonus Feature: Download Results
                clean_df = pd.DataFrame(ranked_jobs)[['title', 'location', 'type', 'match_score', 'missing_skills']]
                csv = clean_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Recommendations (CSV)",
                    data=csv,
                    file_name="job_recommendations.csv",
                    mime="text/csv"
                )
else:
    st.info("👆 Please upload your PDF resume from the sidebar to begin.")
