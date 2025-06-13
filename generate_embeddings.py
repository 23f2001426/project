import os
import json
import requests
from dotenv import load_dotenv
from tqdm import tqdm

# Load .env
load_dotenv()

DISCOURSE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_SLUG = "courses/tds-kb"
CATEGORY_ID = 34
OUTPUT_DIR = "downloaded_threads"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load cookies from .env
cookies = {
    '_t': os.getenv("DISCOURSE_T_COOKIE", ""),
    '_forum_session': os.getenv("DISCOURSE_SESSION_COOKIE", "")
}

def create_authenticated_session(base_url, cookies):
    session = requests.Session()
    domain = base_url.split('//')[1]
    for name, value in cookies.items():
        session.cookies.set(name, value, domain=domain)
    return session

def fetch_all_topic_ids(session, category_id):
    topic_ids = []
    page = 0

    while True:
        url = f"{DISCOURSE_URL}/c/{CATEGORY_SLUG}/{category_id}.json?page={page}"
        response = session.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break
        topic_ids.extend([t["id"] for t in topics])
        page += 1

    return list(set(topic_ids))

def download_topic(session, topic_id, output_dir):
    url = f"{DISCOURSE_URL}/t/{topic_id}.json"
    response = session.get(url)
    if response.status_code == 200:
        topic_data = response.json()
        file_path = os.path.join(output_dir, f"{topic_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(topic_data, f, indent=2)
        return True
    return False

def main():
    session = create_authenticated_session(DISCOURSE_URL, cookies)

    # Test authentication
    test = session.get(f"{DISCOURSE_URL}/session/current.json")
    if test.status_code != 200:
        print("Authentication failed.")
        return
    user = test.json().get("current_user", {}).get("username")
    print(f"Authenticated as: {user}")

    # Fetch all topic IDs from the category
    print(f"Fetching topic IDs from category ID {CATEGORY_ID}...")
    topic_ids = fetch_all_topic_ids(session, CATEGORY_ID)
    print(f"Found {len(topic_ids)} topics.")

    # Download each topic JSON
    print("Downloading topics...")
    for tid in tqdm(topic_ids, desc="Topics"):
        download_topic(session, tid, OUTPUT_DIR)

    print("Download complete. JSON files saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
