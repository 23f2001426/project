import sqlite3

conn = sqlite3.connect("knowledge_base_helper.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM discourse_chunks")
print("Discourse total:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM discourse_chunks WHERE embedding IS NOT NULL")
print("Discourse with embeddings:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM markdown_chunks")
print("Markdown total:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM markdown_chunks WHERE embedding IS NOT NULL")
print("Markdown with embeddings:", cur.fetchone()[0])
