import pytest

from config import Settings

def test_defaults():
    s = Settings(db_password="x")
    assert s.db_port == 5432
    assert s.db_name == "userapi"

def test_env_override(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db.internal")
    s = Settings(db_password="x")
    assert s.db_host == "db.internal"

def test_password_required(monkeypatch):
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    with pytest.raises(Exception):
        Settings(_env_file=None)

def test_db_url():
    s = Settings(db_password="secret", db_host="h", db_name="d")
    assert s.database_url == "postgresql+psycopg2://userapi:secret@h:5432/d"