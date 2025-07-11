from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_jobspresso_jobs(limit=1000):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.5993.71 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.5993.71 Safari/537.36"
    })

    url = "https://jobspresso.co/remote-work/"
    job_list = []

    try:
        driver.get(url)
        time.sleep(5)

        cards = driver.find_elements(By.CLASS_NAME, "job_listing")

        for card in cards[:limit]:
            try:
                title = card.find_element(By.TAG_NAME, "h3").text
            except:
                title = None
            try:
                company = card.find_element(By.CLASS_NAME, "job_listing-company").text
            except:
                company = None
            try:
                location = card.find_element(By.CLASS_NAME, "job_listing-location").text
            except:
                location = "Remote"

            job_list.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": "N/A",
                "salary": "N/A",
                "source": "Jobspresso (Selenium)"
            })
    finally:
        driver.quit()

    return job_list