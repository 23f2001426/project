import os
import re
import sqlite3
from tqdm import tqdm
from datetime import datetime

MARKDOWN_DIR = "markdown_files"
DB_PATH = "knowledge_base.db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markdown_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_title TEXT,
            original_url TEXT,
            downloaded_at TEXT,
            chunk_index INTEGER,
            content TEXT,
            embedding BLOB
        )
    ''')
    conn.commit()

def create_chunks(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    text = re.sub(r'\s+', ' ', text.strip())
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def parse_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title = ""
    url = ""
    content_lines = []

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.lower().startswith("**original url**:"):
            url = line.split(":", 1)[-1].strip()
        else:
            content_lines.append(line)

    full_content = "".join(content_lines).strip()
    return title or os.path.basename(filepath), url, full_content

def insert_markdown_chunks(conn):
    cursor = conn.cursor()
    files = [f for f in os.listdir(MARKDOWN_DIR) if f.endswith(".md")]
    print(f"📄 Found {len(files)} markdown files to process")
    
    total_chunks = 0
    for file in tqdm(files, desc="Inserting markdown chunks"):
        filepath = os.path.join(MARKDOWN_DIR, file)
        title, url, content = parse_markdown_file(filepath)

        if len(content) < 20:
            continue

        chunks = create_chunks(content)
        downloaded_at = datetime.now().isoformat()

        for i, chunk in enumerate(chunks):
            cursor.execute('''
                INSERT INTO markdown_chunks
                (doc_title, original_url, downloaded_at, chunk_index, content, embedding)
                VALUES (?, ?, ?, ?, ?, NULL)
            ''', (title, url, downloaded_at, i, chunk))
            total_chunks += 1

    conn.commit()
    print(f"✅ Inserted {total_chunks} markdown chunks into {DB_PATH}")

def main():
    conn = create_connection()
    create_table(conn)
    insert_markdown_chunks(conn)
    conn.close()

if __name__ == "__main__":
    main()
