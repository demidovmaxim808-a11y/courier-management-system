from typing import List, Optional


class User:
    """Пользователь системы — диспетчер."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        role: str = "диспетчер",
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email
        self.role = role

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
            role=data.get("role", "диспетчер"),
        )

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"{self.name} ({self.role}), email: {self.email}"


def find_user_by_id(
    users: List[User], user_id: int
) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(
    users: List[User], query: str
) -> List[User]:
    """Найти пользователей по имени или email."""
    result = []
    for user in users:
        if query.lower() in user.name.lower() or query.lower() in user.email.lower():
            result.append(user)
    return result


def add_user(
    users: List[User],
    name: str,
    email: str,
    role: str = "диспетчер",
) -> User:
    """Создать объект User и добавить его в коллекцию."""
    new_id = len(users) + 1
    user = User(new_id, name, email, role)
    users.append(user)
    return user


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("\nСписок пользователей пуст.")
        return
    print(f"\nВСЕГО ПОЛЬЗОВАТЕЛЕЙ: {len(users)}")
    print("-" * 50)
    for user in users:
        print(f"  ID {user.id}: {user}")
    print("-" * 50)
