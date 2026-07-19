import pytest
from pydantic import ValidationError

from schemas import UserCreate, UserUpdate

def test_vaild_user():
    u = UserCreate(username="quentin", email="ex@example.com")
    assert u.username == "quentin"

def test_short_username():
    with pytest.raises(ValidationError):
        UserCreate(username="aa", email="ex@example.com")

def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="quentin", email="test")

def test_update_partial():
    payload = UserUpdate(email="other@example.com")