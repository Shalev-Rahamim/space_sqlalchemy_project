```markdown
# 🌌 Galaxy Command: SQL Analytics & Management

A concise CLI application for managing space missions and analytics using **SQLAlchemy ORM** and **PostgreSQL**.  
The project demonstrates CRUD operations, 1:1 / 1:N / N:M relationships, and JOIN‑based business queries.

---

## 🚀 Quick Start

### 1. Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Database Setup

1. Make sure PostgreSQL is running and create a database (e.g. `space_db`).
2. In the project root, create a `.env` file:

```bash
# .env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/space_db
```

`database/connection.py` loads `DATABASE_URL` via `python-dotenv`, so you do **not** need to edit the Python code.

### 3. Initialize & Seed Data

Run the seed script to (re)create tables and insert real + fake data:

```bash
python scripts/seed.py
```

### 4. Run the CLI App

```bash
python main.py
```

---

## 🏗️ Data Model (ORM)

The schema implements all required relationship types:

- **1:1** – `Spacecraft` ↔ `BlackBox` (unique `spacecraft_id` FK, cascade delete).
- **1:N** – `Agency` → `Spacecraft` (an agency owns multiple spacecrafts).
- **N:M** – `Astronaut` ↔ `Mission` via the `mission_assignments` bridge table.

All models are defined in `database/models.py` using SQLAlchemy ORM.

---

## 🧭 CLI Structure

Main menu (`main.py`):

- **Manage Astronauts** – full CRUD:
  - list all, create, update (name + rank), delete.
- **Manage Missions** – full CRUD + relationships:
  - list all, create, update, delete,
  - assign astronauts to missions (N:M).
- **View Agencies Directory**:
  - list all agencies,
  - view spacecrafts per agency.
- **Business Analytics & Reports** – run predefined queries.

Input is validated for numeric IDs and required strings, and database sessions are managed via a context manager (`session_scope`).

---

## 📊 Business Questions Implemented

The service `SpaceAnalyticsService` (`services/queries.py`) exposes 5 business queries:

1. **Agency Fleet Storage** – total black box storage capacity per agency (JOIN + SUM + GROUP BY).
2. **Astronaut Mission Count** – astronauts ranked by number of missions (JOIN + COUNT + ORDER BY).
3. **Agency Fleet Size** – number of spacecrafts per agency (OUTER JOIN + GROUP BY).
4. **Mission Experience** – average crew experience per mission (JOIN + AVG).
5. **Destination Popularity** – most popular destinations by number of missions (GROUP BY + COUNT).

All queries are accessible from the **Business Analytics & Reports** option in the main menu.
```