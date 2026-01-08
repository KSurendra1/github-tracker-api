import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Ensure project root is on sys.path so tests can import `app` package
ROOT = Path(__file__).resolve().parents[1]
# Load project .env so DATABASE_URL and other env vars are available during tests
load_dotenv(ROOT / ".env")
# Optional: expose DATABASE_URL to tests
os.environ.setdefault("DATABASE_URL", os.environ.get("DATABASE_URL", ""))

sys.path.insert(0, str(ROOT))

# Reset database before each test to ensure a clean state when using Postgres
import pytest
from app.core.database import engine, Base

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

