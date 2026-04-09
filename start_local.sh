#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# start_local.sh – One-command local development setup & server launch
# ---------------------------------------------------------------------------
set -e

VENV_DIR="venv"
PYTHON="python3"

echo "=== RentLoop Backend – Local Dev Setup ==="

# 1. Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/5] Creating virtual environment..."
    $PYTHON -m venv $VENV_DIR
else
    echo "[1/5] Virtual environment already exists."
fi

# 2. Activate venv
# shellcheck disable=SC1091
source $VENV_DIR/bin/activate

# 3. Install / upgrade dependencies
echo "[2/5] Installing dependencies..."
pip install -r requirements.txt --quiet

# 4. Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "[3/5] Creating .env from .env.example..."
    cp .env.example .env
else
    echo "[3/5] .env already exists – skipping."
fi

# 5. Run migrations
echo "[4/5] Running database migrations..."
python manage.py migrate

# 6. Create superuser if none exists
echo "[5/5] Checking for superuser..."
python manage.py shell -c "
from users.models import CustomUser
if not CustomUser.objects.filter(is_superuser=True).exists():
    CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('  Superuser created: admin / admin123')
else:
    print('  Superuser already exists.')
"

echo ""
echo "==========================================="
echo "  Starting development server..."
echo "  API:        http://127.0.0.1:8000/api/"
echo "  Swagger UI: http://127.0.0.1:8000/api/docs/"
echo "  ReDoc:      http://127.0.0.1:8000/api/redoc/"
echo "  Admin:      http://127.0.0.1:8000/admin/"
echo "  Login:      admin / admin123"
echo "==========================================="
echo ""
python manage.py runserver
