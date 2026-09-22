from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation() -> None:
    """Проверка создания объекта User."""
    user = User(1, "Иван", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван"
    assert user.email == "ivan@example.com"


def test_user_from_data() -> None:
    """Проверка создания User из данных JSON."""
    data = {"id": 1, "name": "Иван", "email": "ivan@example.com"}
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == "Иван"


def test_user_str() -> None:
    """Проверка строкового представления."""
    user = User(1, "Иван", "ivan@example.com")
    text = str(user)
    assert "Иван" in text
    assert "ivan@example.com" in text


def test_add_user() -> None:
    """Проверка добавления пользователя."""
    users = []
    add_user(users, "Иван", "ivan@example.com")
    assert len(users) == 1


def test_find_user_by_id() -> None:
    """Проверка поиска по ID."""
    users = []
    u = add_user(users, "Иван", "ivan@example.com")
    assert find_user_by_id(users, u.id) is u


def test_find_user() -> None:
    """Проверка поиска по имени и email."""
    users = []
    add_user(users, "Иван", "ivan@example.com")
    add_user(users, "Мария", "maria@example.com")
    assert len(find_user(users, "иван")) == 1
    assert len(find_user(users, "maria")) == 1