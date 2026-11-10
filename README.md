# FastAPI Calculator

A calculator web application. FastAPI serves a page with two number inputs
and four buttons. Each button sends the numbers as JSON to a POST endpoint
(/add, /subtract, /multiply, /divide), the server validates them with
Pydantic, runs the operation, and returns the result as JSON, which the page
displays. Invalid input or division by zero returns a 400 with an error
message instead of crashing. The server logs every calculation and error.

The project also has a user model stored in PostgreSQL through SQLAlchemy,
with Pydantic schemas for validating user input and bcrypt for passwords.

## Setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium

## Run

    python main.py

Then open http://127.0.0.1:8000.

## Tests

The user tests need PostgreSQL running, so start the database first:

    docker compose up -d db
    pytest tests/unit tests/integration
    pytest tests/e2e

- Unit tests call the four functions in app/operations directly, check
  password hashing and verification, and check that the user schemas accept
  good input and reject bad emails, short usernames, and short or overlong
  passwords.
- Integration tests send requests to every endpoint through FastAPI's
  TestClient, including decimals, negatives, missing or non-numeric fields,
  and the home page. The user tests save users to the real database and
  check that duplicate usernames and emails are rejected, that only the hash
  is stored, and that an invalid email never reaches the database.
- End-to-end tests start the server and use Playwright to fill the inputs,
  click each button, and check what the page shows, including the error for
  dividing by zero and for an empty input.

## User model

- app/models/user.py: the users table. username and email are unique,
  password_hash holds the bcrypt hash, and created_at is set by the
  database.
- app/schemas/user.py: UserCreate validates new user data. UserRead is what
  gets returned and has no password field.
- app/security.py: hash_password and verify_password.
- app/database.py: the engine and session. The connection string comes from
  DATABASE_URL and defaults to the local Compose database.

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

## CI/CD

GitHub Actions runs on every push and pull request to main:

1. test: runs the unit, integration, and end-to-end tests against a
   PostgreSQL service container.
2. security: builds the image and scans it with Trivy, failing on critical
   or high vulnerabilities that have a fix.
3. deploy: on main only, pushes the image to Docker Hub.

Docker Hub: https://hub.docker.com/r/chima765432/is601-m10-python-calculator

    docker pull chima765432/is601-m10-python-calculator:latest
    docker run -p 8000:8000 chima765432/is601-m10-python-calculator:latest
