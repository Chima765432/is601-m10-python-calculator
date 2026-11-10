from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead

VALID = {"username": "chima", "email": "chima@example.com", "password": "secret123"}


def test_user_create_accepts_valid_data():
    user = UserCreate(**VALID)
    assert user.email == "chima@example.com"


@pytest.mark.parametrize(
    "field, value",
    [
        ("email", "chima.example.com"),
        ("email", "chima@"),
        ("username", "ab"),
        ("username", "a" * 51),
        ("password", "short"),
        ("password", "a" * 73),
    ],
)
def test_user_create_rejects_bad_values(field, value):
    with pytest.raises(ValidationError):
        UserCreate(**{**VALID, field: value})


def test_user_create_requires_every_field():
    with pytest.raises(ValidationError):
        UserCreate(username="chima", email="chima@example.com")


def test_user_read_leaves_out_the_hash():
    user = User(
        id=1,
        username="chima",
        email="chima@example.com",
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
    )
    data = UserRead.model_validate(user).model_dump()
    assert data["username"] == "chima"
    assert "password_hash" not in data
