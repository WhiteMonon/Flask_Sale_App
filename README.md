# Flask Sale App

A simple Flask application for demonstrating a sales/store management system (products, orders, users, admin utilities).

- Language: Python (Flask)
- Purpose: Example API + simple sales management demo
- Key files:
  - `app.py` — application entrypoint
  - `routes.py` — HTTP routes / API handlers
  - `models.py` — SQLAlchemy models
  - `admin.py` — admin utilities / scripts
  - `ultils.py` — utility functions
  - `sale_app/` — application package (if present)
  - `data/` — static/sample data
  - `migrations/` — DB migration scripts
  - `requirements.txt` — Python dependencies

## Requirements
- Python 3.8+
- A database (SQLite for local dev; PostgreSQL/MySQL for production)
- Environment variables (example):
  - `FLASK_APP=app.py`
  - `FLASK_ENV=development` (optional)
  - `SQLALCHEMY_DATABASE_URI` or `DATABASE_URL`
  - `SECRET_KEY`

## Installation (local)
1. Clone repository
   ```bash
   git clone https://github.com/WhiteMonon/Flask_Sale_App.git
   cd Flask_Sale_App
   ```
2. Create virtual environment and install deps
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set environment variables (example using SQLite)
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SQLALCHEMY_DATABASE_URI="sqlite:///dev.db"
   export SECRET_KEY="change-me"
   ```
4. Run migrations (if project uses Flask-Migrate)
   ```bash
   flask db init        # only if migrations not initialized
   flask db migrate -m "init"
   flask db upgrade
   ```

## Run the application
```bash
flask run --host=0.0.0.0 --port=5000
# or
python app.py
```

## Create an admin user (example)
Adjust to match `models.py` actual model names and methods.

example_create_admin.py:
```python
from app import app, db
from models import User

app.app_context().push()

admin = User(username="admin", email="admin@example.com", is_admin=True)
# If your User model provides a helper for password hashing:
if hasattr(admin, "set_password"):
    admin.set_password("securepassword")
else:
    admin.password = "securepassword"  # replace with hash as needed

db.session.add(admin)
db.session.commit()
print("Admin created")
```

Run:
```bash
python example_create_admin.py
```

## API usage examples (Python)
Replace endpoints with actual routes from `routes.py`.

List products:
```python
import requests

BASE = "http://127.0.0.1:5000"
resp = requests.get(f"{BASE}/api/products")
resp.raise_for_status()
products = resp.json()
for p in products:
    print(p.get("id"), p.get("name"))
```

Login and access protected endpoint (token-based example):
```python
import requests

BASE = "http://127.0.0.1:5000"
login = requests.post(f"{BASE}/api/login", json={"email":"me@example.com","password":"pwd"})
login.raise_for_status()
token = login.json().get("access_token")

headers = {"Authorization": f"Bearer {token}"}
orders = requests.get(f"{BASE}/api/orders", headers=headers)
print(orders.json())
```

## Project structure (quick)
- `app.py` — create Flask app, register blueprints, DB init
- `routes.py` — route handlers, validation, JSON responses
- `models.py` — SQLAlchemy models and helpers
- `admin.py` — admin scripts or admin panel setup
- `ultils.py` — helper utilities
- `migrations/` — DB migration history

## Testing
- (If tests exist) use pytest:
  ```bash
  pytest
  ```

## Logging & Debug
- Use `FLASK_ENV=development` for debug mode.
- Configure logging in `app.py` or a dedicated config file.

## Deployment notes
- Use a WSGI server (gunicorn/uwsgi) in production.
- Set `FLASK_ENV=production` and secure `SECRET_KEY`.
- Use a managed DB and run migrations when deploying.

## Contributing
- Open issues for bugs or feature requests.
- Create pull requests with clear descriptions and tests where applicable.

## License
- Add a `LICENSE` file if you want to specify a license. Repository currently does not include one by default.

---

If you want, I can:
- Tailor the README to match the exact route names and model fields found in your `routes.py` and `models.py`.
- Shorten or expand any section.
