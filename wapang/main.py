from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from wapang.api import api_router
from wapang.app.user.errors import MissingRequiredFieldError

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.exception_handler(RequestValidationError)
def exception_handler(request, exc):
    raise MissingRequiredFieldError()
