from datetime import datetime, timedelta
from classes import Token, User


def test_token_creation():
    user = User("username", "password")
    token = Token("abc123", user, datetime.now())
    assert token.code == "abc123"
    assert token.user == user
    assert isinstance(token.created_at, datetime)


def test_token_expired():
    user = User("username", "password")
    expired_time = datetime.now() - timedelta(minutes=15)
    token = Token("abc123", user, expired_time)
    assert token.is_expired == True


def test_token_not_expired():
    user = User("username", "password")
    valid_time = datetime.now() - timedelta(minutes=5)
    token = Token("abc123", user, valid_time)
    assert token.is_expired == False

