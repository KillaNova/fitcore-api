# FitCore API

A REST API for fitness client management, built with FastAPI and PostgreSQL.

## Features

- Create, read, update, and delete clients
- Track body composition progress per client (weight, body fat percentage, skeletal muscle, muscle mass)
- Persistent data storage with PostgreSQL
- Auto-generated API documentation via Swagger UI

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy 2
- Pydantic 2

## Installation

1. Clone the repository
2. Install dependencies:
   `pip install -r requirements.txt`
3. Set up PostgreSQL and create a database called `fitcore`
4. Copy `.env.example` to `.env` and fill in your `DATABASE_URL`
5. Run the server:
   `uvicorn main:app --reload`

## API Endpoints

Request bodies are JSON.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /clients | Create a new client |
| GET | /clients?skip=0&limit=100 | Get clients (paginated) |
| GET | /clients/{id} | Get one client |
| PUT | /clients/{id} | Update a client's weight and/or goal |
| DELETE | /clients/{id} | Delete a client and their progress |
| POST | /clients/{id}/progress | Add progress entry |
| GET | /clients/{id}/progress | Get progress history (oldest first) |

## Documentation

Run the server and visit http://127.0.0.1:8000/docs for interactive API documentation.

## Roadmap

Planned expansions are marked in the code with `# EXPANSION:` comments, each one explaining what will be added there. List them all with:

`grep -rn "EXPANSION" *.py`

Also planned: automated tests in a `tests/` folder (pytest + FastAPI TestClient).
