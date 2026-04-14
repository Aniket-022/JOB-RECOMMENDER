import requests

def fetch_jobs_from_api(location, job_type, api_key=None):
    """
    Fetch jobs from a Job API like JSearch (via RapidAPI).
    Requires a RapidAPI key.
    
    If no API key is provided, falls back to a mock API.
    """
    if not api_key:
        return get_mock_api_jobs(location, job_type)
        
    url = "https://jsearch.p.rapidapi.com/search"
    query = f"{job_type} in {location}"
    querystring = {"query": query, "page": "1", "num_pages": "1"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status() # Raise exception for 4XX/5XX errors
        data = response.json()
        
        normalized_jobs = []
        for item in data.get("data", []):
            normalized_jobs.append({
                "title": item.get("job_title", "Unknown Title"),
                "skills": [], # Often not explicitly exposed by JSearch, would require NLP on description
                "location": item.get("job_city", location) or location,
                "type": job_type,
                "description": item.get("job_description", "")[:800] # truncate to save memory
            })
        return normalized_jobs
        
    except Exception as e:
        print(f"API fetch error: {e}")
        return []

def get_mock_api_jobs(location, job_type):
    """
    Return fake API data if no API key is provided.
    """
    # Sample real-looking jobs mapped dynamically to the user's location/type preferences
    mock_data = [
        {
            "title": "Software Engineer (External API Source)",
            "skills": ["python", "docker", "aws", "git", "api design"],
            "location": location if location else "Remote",
            "type": job_type if job_type else "Full-time",
            "description": f"We are looking for a highly skilled Software Engineer in {location} to join our growing global team. You will build and scale APIs."
        },
        {
            "title": "Data Analyst (External API Source)",
            "skills": ["sql", "python", "powerbi", "excel", "communication"],
            "location": location if location else "Remote",
            "type": job_type if job_type else "Full-time",
            "description": f"Exciting opportunity for a Data Analyst in {location}! You will be writing SQL queries and visualizing data to drive product decisions."
        }
    ]
    return mock_data
