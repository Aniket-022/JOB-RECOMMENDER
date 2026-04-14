import json
import os

def load_local_jobs(filepath="data/jobs.json"):
    """
    Loads job data from a local JSON file.
    """
    try:
        if not os.path.exists(filepath):
            # Fallback path logic in case it's run from a deeply nested folder
            filepath = os.path.join(os.path.dirname(__file__), "data", "jobs.json")
            
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading local jobs: {e}")
        return []

def filter_jobs(jobs, location, job_type):
    """
    Filter a list of jobs based on location and type preferences.
    """
    filtered = []
    for job in jobs:
        # Check location (case-insensitive) - treat empty as wild card
        job_loc = job.get('location', '').lower()
        pref_loc = location.lower()
        
        # We consider a match if the preferred location is in the job location, 
        # or if preferred location is empty/any
        loc_match = (not pref_loc) or (pref_loc in job_loc) or (job_loc in pref_loc) or (job_loc == "remote")
        
        # Check job type (case-insensitive)
        job_typ = job.get('type', '').lower()
        pref_typ = job_type.lower()
        type_match = (not pref_typ) or (pref_typ in job_typ) or (job_typ in pref_typ)
        
        if loc_match and type_match:
            filtered.append(job)
            
    return filtered
