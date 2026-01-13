from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime, timezone



import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()  # Neon connection string
if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL (Neon Postgres connection string)")

app = FastAPI()

# Serve /static and homepage
app.mount("/static", StaticFiles(directory="static"), name="static")


class ArticleIn(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    author: Optional[str] = ""
    source_name: Optional[str] = "manual"
    url: Optional[str] = ""


@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/submit")
def submit_article(a: ArticleIn):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO articles (title, content, author, source_name, url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, created_at;
                    """,
                    (a.title, a.content, a.author or "", a.source_name or "manual", a.url or ""),
                )
                row = cur.fetchone()
                conn.commit()
        return {"ok": True, "id": str(row["id"]), "created_at": row["created_at"].isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {e}")


@app.get("/ping")
def ping():
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}