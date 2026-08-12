# Books to Scrape — Async Playwright Scraper

An educational web-scraping project built with **Python, Playwright, PostgreSQL, SQLAlchemy, FastAPI, Alembic, and Docker**.

The project started as a basic scraper and was progressively upgraded into an asynchronous, database-backed application using a producer-consumer architecture.

> **Note:** Books to Scrape is intentionally designed for scraping practice. This project is primarily a learning project for building a complete scraping pipeline rather than a real-world anti-bot scraping system.

---

## Features

* Asynchronous scraping with Playwright
* Multiple concurrent scraper workers
* `asyncio.Queue` producer-consumer architecture
* Book listing and detail-page scraping
* Retry handling for failed operations
* Structured logging
* CSV and JSON output
* PostgreSQL persistence
* SQLAlchemy ORM/database access
* FastAPI REST API
* Alembic database migrations
* Docker and Docker Compose
* Database-level duplicate prevention
* Idempotent database insertion using PostgreSQL `ON CONFLICT DO NOTHING`
* Automated tests for scraper/API components

---

## Architecture

```text
                    Docker Compose
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     books-api      books-scraper    books-db
      FastAPI        Playwright     PostgreSQL
          │              │              │
          └──────────────┴──────────────┘
                         │
                         ▼
                    PostgreSQL
```

### Scraper architecture

```text
Listing Pages
      │
      ▼
Collect book URLs
      │
      ▼
 asyncio.Queue
      │
 ┌────┼────┐
 ▼    ▼    ▼
W1   W2   W3
 │    │    │
 └────┼────┘
      ▼
Book detail pages
      │
      ▼
Parse data
      │
      ▼
PostgreSQL / CSV / JSON
```

The listing stage acts as the producer and the asynchronous workers act as consumers.

---

## Technologies

* Python 3.14
* Playwright
* asyncio
* SQLAlchemy
* PostgreSQL
* FastAPI
* Alembic
* Docker
* Docker Compose
* pytest
* Rich

---

## Project Structure

```text
books_to_scrape/
├── api/                 # FastAPI application and routes
├── database/            # Database connection, models and repository
├── scraper/             # Async scraper and workers
├── storage/             # CSV/JSON storage
├── utils/               # Retry and progress utilities
├── tests/               # Automated tests
├── alembic/             # Database migrations
├── config.py            # Application configuration
├── logger_config.py     # Logging configuration
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Database

The project uses PostgreSQL for persistent storage.

Two main tables are used:

```text
basic_data
advanced_data
```

The `advanced_data.upc` column has a unique constraint:

```text
UNIQUE(upc)
```

This prevents the database from storing duplicate books with the same UPC.

### Idempotent insertion

The repository uses PostgreSQL conflict handling:

```python
stmt = insert(AdvancedData).values(**record)

stmt = stmt.on_conflict_do_nothing(
    index_elements=["upc"]
)
```

Therefore, if the scraper encounters a book that has already been stored, the duplicate is safely ignored instead of causing an unhandled database error.

---

## Docker Services

Docker Compose runs three services:

### API

```text
books-api
```

Runs FastAPI on port `8000`.

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Database

```text
books-db
```

Runs PostgreSQL.

The container uses port `5432` internally and is exposed to the host on:

```text
5433
```

### Scraper

```text
books-scraper
```

Runs the Playwright-based scraper.

The scraper and API communicate with PostgreSQL through the Docker Compose network using:

```text
db:5432
```

The application must not use `localhost` for the Docker PostgreSQL service.

---

## Configuration

Configuration is provided through environment variables.

Example:

```text
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
```

Do not commit real passwords, API keys, or other secrets to Git.

Use `.env` for local configuration.

---

## Running with Docker

Build and start the services:

```bash
docker compose up -d --build
```

Check services:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs api
```

View scraper logs:

```bash
docker compose logs scraper
```

View database logs:

```bash
docker compose logs db
```

Stop the services:

```bash
docker compose down
```

---

## Database Migrations

Alembic is used to manage database schema changes.

Create a migration:

```bash
alembic revision -m "migration message"
```

View migration history:

```bash
alembic history
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

Migration files are stored in:

```text
alembic/versions/
```

---

## Running the Scraper

The scraper is a Python package and should be executed using module syntax:

```bash
docker compose exec api python -m scraper.main
```

A dedicated scraper service is also available:

```bash
docker compose run --rm scraper python -m scraper.main
```

---

## Useful Docker Commands

Open a shell in the API container:

```bash
docker compose exec api bash
```

Run Python inside the API container:

```bash
docker compose exec api python
```

Execute a PostgreSQL query:

```bash
docker compose exec db psql -U postgres -d books_to_scrape
```

Check for duplicate UPCs:

```bash
docker compose exec db psql -U postgres -d books_to_scrape \
-c "SELECT upc, COUNT(*) FROM advanced_data GROUP BY upc HAVING COUNT(*) > 1;"
```

Rebuild an image:

```bash
docker compose up -d --build
```

Force a completely fresh build:

```bash
docker compose build --no-cache
```

---

## Learning Outcomes

This project was used to practice:

* Python asynchronous programming
* Playwright browser automation
* Producer-consumer architectures
* Concurrent scraping workers
* Retry and error handling
* Logging
* SQLAlchemy
* PostgreSQL
* FastAPI
* REST API development
* Database migrations with Alembic
* Database constraints
* Idempotent database operations
* Docker and Docker Compose
* Basic automated testing
* Structuring a Python application into separate components

---

## Project Purpose

Books to Scrape is a deliberately simple website designed for learning web scraping.

The main goal of this project was to learn how to build a complete scraping application and understand how its components fit together:

```text
Scraping
   ↓
Processing
   ↓
Database
   ↓
API
   ↓
Docker
   ↓
Testing
```

The project is not intended to represent the full complexity of production web scraping against modern anti-bot systems.

---

## Disclaimer

This project was created for educational purposes using Books to Scrape, a website designed for practicing web scraping.
