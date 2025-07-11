import requests
from bs4 import BeautifulSoup

def scrape_jobspresso_jobs(limit=5):
    """
    Scrapes job listings from jobspresso.co.
    """
    url = "https://jobspresso.co/remote-work/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        print("❌ Failed to load Jobspresso page")
        return []

    soup = BeautifulSoup(response.content, "lxml")
    jobs = soup.find_all("li", class_="job_listing")
    job_list = []

    for job in jobs[:limit]:
        title_tag = job.find("h3")
        company_tag = job.find("div", class_="job_listing-company")
        location_tag = job.find("div", class_="job_listing-location")

        job_list.append({
            "title": title_tag.text.strip() if title_tag else None,
            "company": company_tag.text.strip() if company_tag else None,
            "location": location_tag.text.strip() if location_tag else "Remote",
            "date_posted": "N/A",
            "salary": "N/A",
            "source": "Jobspresso"
        })

    return job_list