# generate_embeddings.py
import sqlite3
import json
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_PATH = "knowledge_base.db"
BATCH_SIZE = 100  # Tune if rate-limited

async def get_embedding(openai_input):
    url = "https://aipipe.org/openai/v1/embeddings"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": openai_input
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["data"][0]["embedding"]

async def process_batch(chunks):
    async with aiohttp.ClientSession() as session:
        for chunk_id, content in chunks:
            embedding = await get_embedding(content)
            yield chunk_id, embedding

async def main():
    if not API_KEY:
        print("Error: API_KEY missing")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM discourse_chunks WHERE embedding IS NULL")
    all_rows = cur.fetchall()
    print(f"Found {len(all_rows)} chunks without embeddings")

    for i in range(0, len(all_rows), BATCH_SIZE):
        batch = all_rows[i:i + BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch)} chunks)")
        async for chunk_id, embedding in process_batch(batch):
            cur.execute(
                "UPDATE discourse_chunks SET embedding = ? WHERE id = ?",
                (json.dumps(embedding), chunk_id)
            )
        conn.commit()

    conn.close()
    print(" Done generating embeddings")


if __name__ == "__main__":
    asyncio.run(main())
