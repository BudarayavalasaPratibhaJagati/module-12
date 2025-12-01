# Module 12 – FastAPI Calculator Backend

This project is the **Module 12 backend** for a calculator web application.  
It provides:

- **User registration and login** with hashed passwords
- **Calculation CRUD (BREAD) APIs** for basic arithmetic operations
- **Pydantic validation** (including divide-by-zero checks)
- **Automated tests** with `pytest`
- **CI/CD with GitHub Actions** and Docker image builds for deployment

---

## Tech Stack

- **Language:** Python 3.11+ (tested with 3.13)
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic v2
- **Database (local dev):** SQLite (`app.db`)
- **Testing:** pytest + FastAPI TestClient
- **Containerization:** Docker
- **CI/CD:** GitHub Actions (runs tests and builds Docker image)

---

## Project Structure

```text
app/
  main.py               # FastAPI application entrypoint
  database.py           # SQLAlchemy engine and session
  models.py             # SQLAlchemy models: User, Calculation
  schemas.py            # Pydantic schemas: UserCreate, UserRead, CalculationCreate, CalculationRead
  security.py           # Password hashing & verification
  routers/
    users.py            # /users/register, /users/login
    calculations.py     # /calculations BREAD endpoints

tests/
  test_calculation_integration.py
  test_calculation_unit.py
  test_calculations_integration.py
  test_users_integration.py

requirements.txt
Dockerfile
.github/workflows/ci.yml   # GitHub Actions pipeline (if present)
