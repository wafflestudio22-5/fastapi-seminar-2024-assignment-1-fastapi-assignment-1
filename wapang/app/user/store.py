from functools import cache
from wapang.app.user.errors import EmailAlreadyExistsError, UsernameAlreadyExistsError
from wapang.app.user.models import User


class UserStore:
    def __init__(self) -> None:
        self.id_counter = 0
        self.store: dict[int, User] = {}
        self.username_index: dict[str, int] = {}
        self.email_index: dict[str, int] = {}

    def add_user(self, username: str, password: str, email: str) -> User:
        if self.get_user_by_username(username):
            raise UsernameAlreadyExistsError()

        if self.get_user_by_email(email):
            raise EmailAlreadyExistsError()

        self.id_counter += 1
        user = User(
            id=self.id_counter, username=username, password=password, email=email
        )
        self.store[user.id] = user
        self.username_index[user.username] = user.id
        self.email_index[user.email] = user.id
        return user.model_copy()

    def get_user_by_username(self, username: str) -> User | None:
        user_id = self.username_index.get(username)
        if not user_id:
            return None
        return self.store[user_id].model_copy()

    def get_user_by_email(self, email: str) -> User | None:
        user_id = self.email_index.get(email)
        if not user_id:
            return None
        return self.store[user_id].model_copy()

    def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        user = self.get_user_by_username(username)
        if not user:
            raise ValueError(f"User {username} does not exist")

        if email:
            if self.get_user_by_email(email):
                raise ValueError(f"Email {email} already exists")
            self.email_index.pop(user.email)
            self.email_index[email] = user.id
            user.email = email

        if address:
            user.address = address

        if phone_number:
            user.phone_number = phone_number

        return user


@cache
def get_user_store() -> UserStore:
    return UserStore()
