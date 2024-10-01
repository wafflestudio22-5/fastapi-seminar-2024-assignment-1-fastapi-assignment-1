from fastapi import HTTPException


class EmailAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(409, "Email already exists")

class UsernameAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(409, "Username already exists")

class InvalidFieldFormatError(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid field format")

class MissingRequiredFieldError(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Missing required field")
