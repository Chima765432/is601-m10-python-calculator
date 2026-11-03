# FastAPI Calculator

A calculator web application. FastAPI serves a page with two number inputs
and four buttons. Each button sends the numbers as JSON to a POST endpoint
(/add, /subtract, /multiply, /divide), the server validates them with
Pydantic, runs the operation, and returns the result as JSON, which the page
displays. Invalid input or division by zero returns a 400 with an error
message instead of crashing. The server logs every calculation and error.

## Setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium

## Run

    python main.py

Then open http://127.0.0.1:8000.

## Tests

    pytest tests/unit tests/integration
    pytest tests/e2e

- Unit tests call the four functions in app/operations directly.
- Integration tests send requests to every endpoint through FastAPI's
  TestClient, including decimals, negatives, missing or non-numeric fields,
  and the home page.
- End-to-end tests start the server and use Playwright to fill the inputs,
  click each button, and check what the page shows, including the error for
  dividing by zero and for an empty input.

GitHub Actions runs all three on every push and pull request to main.

## Database with Docker Compose

    docker compose up --build -d

This starts three containers: the calculator on port 8000, PostgreSQL 16 on
port 5432 (user postgres, password postgres, database fastapi_db), and
pgAdmin at http://localhost:5050 (admin@example.com / admin). The database
server is already registered in pgAdmin through pgadmin/servers.json, using
the host name db, which is how containers on the same Compose network reach
each other. pgAdmin asks for the password, postgres, the first time you open
it.

sql/calculations.sql holds the SQL run in pgAdmin's Query Tool: a users
table and a calculations table linked one-to-many by a user_id foreign key
with ON DELETE CASCADE, followed by inserts, selects, a join, an update, and a
delete.
