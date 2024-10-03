from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from wapang.app.user.dto.requests import UserSignupRequest, UserUpdateRequest
from wapang.app.user.dto.responses import MyProfileResponse
from wapang.app.user.models import User
from wapang.app.user.service import UserService

user_router = APIRouter()


def login_with_header(
    x_wapang_username: Annotated[str, Header(...)],
    x_wapang_password: Annotated[str, Header(...)],
    user_service: Annotated[UserService, Depends()],
) -> User:
    user = user_service.get_user_by_username(x_wapang_username)
    if not user or user.password != x_wapang_password:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


@user_router.post("/signup", status_code=HTTP_201_CREATED)
def signup(
    signup_request: UserSignupRequest, user_service: Annotated[UserService, Depends()]
):
    user_service.add_user(
        signup_request.username, signup_request.password, signup_request.email
    )
    return "Success"


@user_router.get("/me", status_code=HTTP_200_OK)
def me(user: Annotated[User, Depends(login_with_header)]) -> MyProfileResponse:
    return MyProfileResponse.from_user(user)


@user_router.patch("/me", status_code=HTTP_200_OK)
def update_me(
    user: Annotated[User, Depends(login_with_header)],
    update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()],
):
    user_service.update_user(
        user.username,
        email=update_request.email,
        address=update_request.address,
        phone_number=update_request.phone_number,
    )
    return "Success"
