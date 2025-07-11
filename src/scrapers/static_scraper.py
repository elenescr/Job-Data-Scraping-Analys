import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
PROXIES = [
    "http://200.25.254.193:54240",
    "http://45.167.125.97:9992",
    "http://103.169.255.10:3127",
    "http://185.189.199.75:23500",
    "http://103.151.20.133:80",
    "http://103.167.34.3:8080"
]


def get_random_proxy():
    return {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/92.0.4515.159 Safari/537.36"
]



# --------------------------------------
# RemoteOK API Scraper

def scrape_remoteok_jobs(limit=1000):
    url = "https://remoteok.com/api"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    job_list = []

    time.sleep(random.uniform(1.5, 3.0))
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()[1:]
    for job in data[:limit]:
        job_list.append({
            "title": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location") or "Remote",
            "date_posted": job.get("date") or job.get("posted_at"),
            "salary": job.get("salary") or "N/A",
            "source": "RemoteOK"
        })

    return job_list

