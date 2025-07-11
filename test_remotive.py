from src.scrapers.remotive_selenium_scraper import scrape_remotive_jobs

if __name__ == "__main__":
    jobs = scrape_remotive_jobs(limit=5)
    print(f"✅ Found {len(jobs)} jobs from Remotive (Selenium)")
    for job in jobs:
        print(f"- {job['title']} at {job['company']} [{job['location']}]")
