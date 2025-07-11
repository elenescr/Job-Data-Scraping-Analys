import requests

def scrape_remotive_jobs(limit=5):
    """
    Scrapes remote jobs from Remotive.io public API.
    Returns a list of job dictionaries.
    """
    url = "https://remotive.io/api/remote-jobs"
    response = requests.get(url)
    data = response.json()

    job_list = []
    for job in data["jobs"][:limit]:
        job_list.append({
            "title": job["title"],
            "company": job["company_name"],
            "location": job["candidate_required_location"],
            "date_posted": job["publication_date"],
            "salary": job.get("salary", "N/A"),
            "source": "Remotive"
        })
    return job_list