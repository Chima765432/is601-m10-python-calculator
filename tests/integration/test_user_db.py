import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.security import hash_password, verify_password


def save_user(db, username="chima", email="chima@example.com", password="secret123"):
    data = UserCreate(username=username, email=email, password=password)
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    return user


def test_saved_user_gets_an_id_and_created_at(db):
    user = save_user(db)
    assert user.id is not None
    assert user.created_at is not None


def test_database_stores_the_hash_not_the_password(db):
    save_user(db)
    stored = db.query(User).filter_by(username="chima").one()
    assert stored.password_hash != "secret123"
    assert verify_password("secret123", stored.password_hash)


def test_user_read_from_a_stored_user(db):
    user = save_user(db)
    data = UserRead.model_validate(user).model_dump()
    assert data["email"] == "chima@example.com"
    assert "password_hash" not in data


def test_duplicate_username_is_rejected(db):
    save_user(db)
    with pytest.raises(IntegrityError):
        save_user(db, email="other@example.com")


def test_duplicate_email_is_rejected(db):
    save_user(db)
    with pytest.raises(IntegrityError):
        save_user(db, username="other")


def test_invalid_email_never_reaches_the_database(db):
    with pytest.raises(ValidationError):
        save_user(db, email="not-an-email")
    assert db.query(User).count() == 0
