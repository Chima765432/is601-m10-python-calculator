from app.security import hash_password, verify_password


def test_hash_is_not_the_plain_password():
    assert hash_password("secret123") != "secret123"


def test_same_password_gets_a_new_salt_each_time():
    assert hash_password("secret123") != hash_password("secret123")


def test_verify_accepts_the_right_password():
    assert verify_password("secret123", hash_password("secret123")) is True


def test_verify_rejects_the_wrong_password():
    assert verify_password("secret124", hash_password("secret123")) is False
