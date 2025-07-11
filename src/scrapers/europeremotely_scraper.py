import requests
from bs4 import BeautifulSoup
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/92.0.4515.159 Safari/537.36"
]

def scrape_europe_remotely_jobs(limit=5):
    url = "https://europeremotely.com/remote-jobs"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    time.sleep(random.uniform(1.5, 3.0))
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch EuropeRemotely: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "lxml")
    jobs = soup.find_all("div", class_="job")[:limit]
    job_list = []

    for job in jobs:
        title_tag = job.find("h2")
        company_tag = job.find("h3")
        location = "Remote"  # site only shows remote jobs

        job_list.append({
            "title": title_tag.text.strip() if title_tag else None,
            "company": company_tag.text.strip() if company_tag else None,
            "location": location,
            "date_posted": "N/A",
            "salary": "N/A",
            "source": "EuropeRemotely"
        })

    return job_list