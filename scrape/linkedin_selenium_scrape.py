from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from scrape.base import Scraper

load_dotenv()
EMAIL = os.getenv("LINKEDIN_USERNAME")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
PROFILE_URL = "https://www.linkedin.com/in/probe-ai/"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

if not EMAIL or not PASSWORD:
    raise ValueError("LINKEDIN username or password is not set in the environment variables.")


class SeleniumLinkedinScraper(Scraper):
    def read(self, url: str, delay: int = 20) -> str:
        global driver
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            time.sleep(delay)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup.body.get_text(separator='\n', strip=True)
        except Exception as e:
            print(f"Error retrieving content from {url}: {e}")
            return ""
        finally:
            driver.quit()

    def scrape_linkedin(self, url: str) -> str:
        global driver
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            driver.find_element(By.ID, "username").send_keys(EMAIL)
            driver.find_element(By.ID, "password").send_keys(PASSWORD)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)
            driver.get(url)
            time.sleep(5)

            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            main_content = soup.find('main', {'class': 'scaffold-layout__main'})
            if main_content:
                text_content = main_content.get_text(separator='\n', strip=True)
            else:
                text_content = "No content found under the specified class."
            return text_content
        except Exception as e:
            print(f"Error scraping LinkedIn page: {e}")
            return ""
        finally:
            driver.quit()

