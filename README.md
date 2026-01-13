
# Article Uploader (Data Ingestion Service)

A lightweight **data ingestion service** that lets you submit articles via a web UI and stores them in **Neon (Postgres)**.
This project is intentionally scoped to **ingestion only** and is designed to act as the first step in a larger streaming or AI pipeline (e.g., Pathway, embeddings, RAG).

---

## ✨ Features

* 📝 Clean, professional HTML UI for submitting articles
* 🚀 FastAPI backend
* 🗄️ Persistent storage in Neon (Postgres)
* 🔐 Environment-variable–based configuration
* ⚙️ Ready to be consumed by downstream processors (Pathway, ETL, etc.)
* ☁️ Easy to host on Render / Railway / Fly.io

---

## 🏗️ Architecture

```
Browser (HTML UI)
      ↓
FastAPI Backend
      ↓
Neon Postgres
```

> This service **only ingests data**.
> Processing, embeddings, indexing, or RAG are handled by a separate pipeline.

---

## 📁 Project Structure

```
article-uploader/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .gitignore
└── static/
    └── index.html       # Article submission UI
```

---

## 🗄️ Database Schema

Create the table in Neon **once**:

```sql
CREATE TABLE IF NOT EXISTS articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  author TEXT NOT NULL DEFAULT '',
  source_name TEXT NOT NULL DEFAULT 'manual',
  url TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 🔧 Setup (Local)

### 1️⃣ Clone the repo

```bash
git clone <your-repo-url>
cd article-uploader
```

---

### 2️⃣ Create `.env`

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DB?sslmode=require
```

⚠️ **Never commit `.env`**
Make sure it is listed in `.gitignore`.

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the server

```bash
uvicorn main:app --reload --port 8000
```

Open in your browser:

```
http://localhost:8000
```

---

## 🧪 API Endpoints

### `GET /`

Serves the article submission UI.

---

### `POST /submit`

**Request body**

```json
{
  "title": "Article title",
  "content": "Full article content",
  "author": "Optional author",
  "source_name": "manual",
  "url": "https://example.com"
}
```

**Response**

```json
{
  "ok": true,
  "id": "uuid",
  "created_at": "2026-01-12T12:34:56Z"
}
```

---

### `GET /health`

Health check endpoint.

---

## ☁️ Hosting

This service can be deployed as a **single web service**.

### Recommended platforms

* Render
* Railway
* Fly.io

**Start command**

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

Set `DATABASE_URL` as an environment variable in the hosting dashboard.

---

## 🔒 Security Notes

* Rotate database passwords if accidentally exposed
* Protect the UI with auth if used publicly
* Rate-limit `/submit` if opening to external users

---

## 🔮 Downstream Usage

This project is typically paired with a **separate processing service**, such as:

* Pathway streaming pipeline
* Embedding + vector indexing
* RAG / LLM-based systems
* ETL or analytics workflows

Neon Postgres acts as the **contract** between ingestion and processing.

---

## 🎯 Scope (Intentional)

**This repo does NOT include:**

* Pathway
* LLMs
* Embeddings
* Vector databases
* Data processing logic

It is designed to do **one thing well**: **reliable article ingestion**.

---



Just tell me 👍
