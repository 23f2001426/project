import os
import sqlite3
import json
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_PATH = "knowledge_base.db"
BATCH_SIZE = 50

async def get_embedding(text):
    url = "https://aipipe.org/openai/v1/embeddings"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": text
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["data"][0]["embedding"]

async def process_batch(rows):
    results = []
    for row_id, content in rows:
        try:
            emb = await get_embedding(content)
            results.append((row_id, emb))
        except Exception as e:
            print(f"❌ Embed failed for id={row_id}: {e}")
    return results

async def main():
    if not API_KEY:
        print("❌ Missing API_KEY in .env")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM markdown_chunks WHERE embedding IS NULL")
    rows = cur.fetchall()
    print(f"📦 {len(rows)} markdown chunks to embed")

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i+BATCH_SIZE]
        print(f"⚙️  Processing batch {i//BATCH_SIZE + 1}")
        updates = await process_batch(batch)
        for row_id, emb in updates:
            cur.execute("UPDATE markdown_chunks SET embedding = ? WHERE id = ?", (json.dumps(emb), row_id))
        conn.commit()

    conn.close()
    print("✅ All markdown embeddings saved.")

if __name__ == "__main__":
    asyncio.run(main())
