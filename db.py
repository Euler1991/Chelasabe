# db.py — Capa de base de datos para Chelasabe
import json
import os
import sqlite3
from pathlib import Path

DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    try:
        import psycopg2
        import psycopg2.extras

        def get_conn():
            return psycopg2.connect(DATABASE_URL, sslmode="require")

        def init_db():
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_avanzados (
                    id          SERIAL PRIMARY KEY,
                    nombre      TEXT NOT NULL,
                    created_at  TIMESTAMPTZ DEFAULT NOW(),
                    ratings_com JSONB NOT NULL,
                    prefs       JSONB NOT NULL,
                    ratings_est JSONB NOT NULL
                )
            """)
            conn.commit()
            cur.close()
            conn.close()

        def save_advanced_user(nombre, ratings_com, prefs, ratings_est):
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO usuarios_avanzados (nombre, ratings_com, prefs, ratings_est)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (nombre, json.dumps(ratings_com), json.dumps(prefs), json.dumps(ratings_est)),
            )
            row_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return row_id

        def get_advanced_users():
            conn = get_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT id, nombre, ratings_com, prefs, ratings_est FROM usuarios_avanzados")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                {
                    "id": r["id"],
                    "nombre": r["nombre"],
                    "ratings_com": r["ratings_com"],
                    "prefs": r["prefs"],
                    "ratings_est": r["ratings_est"],
                }
                for r in rows
            ]

        POSTGRES_IMPORT_ERROR = None

    except Exception as e:
        POSTGRES_IMPORT_ERROR = str(e)
        USE_POSTGRES = False

else:
    POSTGRES_IMPORT_ERROR = None

if not USE_POSTGRES:
    DB_PATH = Path("chelasabe.db")

    def get_conn():
        return sqlite3.connect(DB_PATH)

    def init_db():
        conn = get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_avanzados (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                ratings_com TEXT NOT NULL,
                prefs       TEXT NOT NULL,
                ratings_est TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_advanced_user(nombre, ratings_com, prefs, ratings_est):
        conn = get_conn()
        cur = conn.execute(
            """INSERT INTO usuarios_avanzados (nombre, ratings_com, prefs, ratings_est)
               VALUES (?, ?, ?, ?)""",
            (nombre, json.dumps(ratings_com), json.dumps(prefs), json.dumps(ratings_est)),
        )
        conn.commit()
        row_id = cur.lastrowid
        conn.close()
        return row_id

    def get_advanced_users():
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, nombre, ratings_com, prefs, ratings_est FROM usuarios_avanzados"
        ).fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "nombre": r["nombre"],
                "ratings_com": json.loads(r["ratings_com"]),
                "prefs": json.loads(r["prefs"]),
                "ratings_est": json.loads(r["ratings_est"]),
            }
            for r in rows
        ]