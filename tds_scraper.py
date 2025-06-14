import os
import time
from urllib.parse import urljoin, unquote
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from markdownify import markdownify as md

BASE_URL = "https://tds.s-anand.net/"
ROOT_PATH = "#/2025-01/"
START_URL = urljoin(BASE_URL, ROOT_PATH)
EXPORT_DIR = "markdown_files"

os.makedirs(EXPORT_DIR, exist_ok=True)

# Headless Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# Track visited URLs
visited = set()
queue = deque()

# Start with the root URL
queue.append(START_URL)
visited.add(START_URL)

def sanitize_filename(href):
    part = unquote(href.split("#/../")[-1] if "#/../" in href else href.split("#/")[1])
    return part.replace("/", "-") + ".md"

def is_valid_internal_link(href):
    return href and href.startswith("https://tds.s-anand.net/#/../")

while queue:
    current_url = queue.popleft()
    print(f"🌐 Visiting: {current_url}")

    try:
        driver.get(current_url)
        time.sleep(2.5)  # wait for JS to render

        # Extract title + main content
        title = driver.title.strip().replace("Tools in Data Science - ", "")
        content_el = driver.find_element(By.CLASS_NAME, "markdown-section")
        content_html = content_el.get_attribute("innerHTML")
        markdown_text = md(content_html)

        # Save markdown
        filename = sanitize_filename(current_url)
        filepath = os.path.join(EXPORT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"**Original URL**: {current_url}\n\n")
            f.write(markdown_text)
        print(f"✅ Saved: {filename}")

        # Extract internal links from the current page
        anchors = driver.find_elements(By.TAG_NAME, "a")
        for a in anchors:
            href = a.get_attribute("href")
            if is_valid_internal_link(href) and href not in visited:
                visited.add(href)
                queue.append(href)
                print(f"➕ Queued: {href}")

    except Exception as e:
        print(f"❌ Failed to scrape {current_url}: {e}")

driver.quit()
print("🎉 BFS crawl completed.")
