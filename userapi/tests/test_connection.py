import pytest
from sqlalchemy import text

from database import engine

@pytest.mark.integration
def test_db_connection():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1