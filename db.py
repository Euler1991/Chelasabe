# db.py — Capa de base de datos SQLite para Chelasabe
import sqlite3
import json
from pathlib import Path

DB_PATH = Path("chelasabe.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Crea las tablas si no existen."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_avanzados (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                ratings_com TEXT NOT NULL,   -- JSON: {cerveza_id: 0-5}
                prefs       TEXT NOT NULL,   -- JSON: color, abv, amargor, cuerpo, aroma[], sabor[]
                ratings_est TEXT NOT NULL    -- JSON: {estilo_id: 0-5}
            )
        """)
        conn.commit()


def save_advanced_user(nombre: str, ratings_com: dict, prefs: dict, ratings_est: dict) -> int:
    """Guarda un usuario avanzado y devuelve su ID."""
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO usuarios_avanzados (nombre, ratings_com, prefs, ratings_est)
               VALUES (?, ?, ?, ?)""",
            (
                nombre,
                json.dumps(ratings_com),
                json.dumps(prefs),
                json.dumps(ratings_est),
            ),
        )
        conn.commit()
        return cur.lastrowid


def get_advanced_users() -> list[dict]:
    """Devuelve todos los usuarios avanzados como lista de dicts."""
    with get_conn() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, nombre, ratings_com, prefs, ratings_est FROM usuarios_avanzados"
        ).fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "nombre": row["nombre"],
            "ratings_com": json.loads(row["ratings_com"]),
            "prefs": json.loads(row["prefs"]),
            "ratings_est": json.loads(row["ratings_est"]),
        })
    return result
