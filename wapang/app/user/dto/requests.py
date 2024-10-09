from functools import wraps
import re
from typing import Annotated, Callable, TypeVar
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator

from wapang.app.user.errors import InvalidFieldFormatError

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+@[a-z]+\.[a-z]+$")


def validate_username(value: str) -> str:
    if not re.match(USERNAME_PATTERN, value):
        raise InvalidFieldFormatError()
    return value


def validate_email(value: str) -> str:
    if not re.match(EMAIL_PATTERN, value):
        raise InvalidFieldFormatError()
    return value


def validate_password(value: str) -> str:
    if len(value) < 8 or len(value) > 20:
        raise InvalidFieldFormatError()

    contains_uppercase = False
    contains_lowercase = False
    contains_digit = False
    contains_special = False

    for char in value:
        if char.isupper():
            contains_uppercase = True
        elif char.islower():
            contains_lowercase = True
        elif char.isdigit():
            contains_digit = True
        else:
            contains_special = True

    constraints_cardinality = sum(
        [contains_uppercase, contains_lowercase, contains_digit, contains_special]
    )
    if constraints_cardinality < 2:
        raise InvalidFieldFormatError()

    return value


T = TypeVar("T")


def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper


def validate_address(value: str) -> str:
    if len(value) > 100:
        raise InvalidFieldFormatError()
    return value


def validate_phone_number(value: str) -> str:
    if not value.startswith("010") or not len(value) == 11 or not value.isdigit():
        raise InvalidFieldFormatError()
    return value


class UserSignupRequest(BaseModel):
    username: Annotated[str, AfterValidator(validate_username)]
    email: Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_password)]


class UserUpdateRequest(BaseModel):
    email: Annotated[str | None, AfterValidator(skip_none(validate_email))] = None
    address: Annotated[str | None, AfterValidator(skip_none(validate_address))] = None
    phone_number: Annotated[
        str | None, AfterValidator(skip_none(validate_phone_number))
    ] = None
