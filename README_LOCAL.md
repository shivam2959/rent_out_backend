# RentLoop Backend – Run Locally

This is the Django REST API backend for [rentloop.in](https://rentloop.in).

---

## Quick Start (one command)

```bash
chmod +x start_local.sh
./start_local.sh
```

That script will:
1. Create a Python virtual environment (`venv/`)
2. Install all dependencies from `requirements.txt`
3. Copy `.env.example` → `.env` (if not already present)
4. Run all database migrations (uses SQLite by default)
5. Create a default superuser (`admin` / `admin123`)
6. Start the dev server on `http://127.0.0.1:8000`

---

## Manual Steps

```bash
# 1. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env              # edit values if needed

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

---

## Local URLs

| Page | URL |
|------|-----|
| API root | http://127.0.0.1:8000/api/ |
| Swagger UI (interactive docs) | http://127.0.0.1:8000/api/docs/ |
| ReDoc | http://127.0.0.1:8000/api/redoc/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

---

## API Endpoints

| Module | Prefix |
|--------|--------|
| Auth (register / login / JWT) | `/api/auth/` |
| Properties (buildings & rooms) | `/api/properties/` |
| Tenants (onboarding) | `/api/tenants/` |
| Leases | `/api/leases/` |
| Payments | `/api/payments/` |
| Reviews | `/api/reviews/` |
| Maintenance requests | `/api/maintenance/` |
| Dashboard | `/api/dashboard/` |

---

## Environment Variables (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | dev key | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DATABASE_URL` | SQLite | Override with PostgreSQL URL for prod |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Frontend origin(s) |

---

## Requirements

- Python 3.10+
- No Redis or PostgreSQL needed for local development (SQLite is used by default)
