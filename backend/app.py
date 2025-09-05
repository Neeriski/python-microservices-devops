from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
LOG_PATH = os.getenv("LOG_PATH", "/shared/requests.log")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

def init_db():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );
            """)
            conn.commit()
    except Exception as e:
        print("DB init error:", e)

@app.route("/api/data")
def data():
    init_db()
    count = 0
    try:
        with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) AS c FROM users;")
            count = cur.fetchone()["c"]
    except Exception as e:
        return jsonify({"status": "ok", "db_error": str(e)}), 200

    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("hit /api/data\n")
    except Exception as e:
        print("log write failed:", e)

    return jsonify({"message": "Hello from backend", "user_count": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
