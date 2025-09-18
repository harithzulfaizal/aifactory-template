from pydantic import BaseModel
from fastapi import HTTPException


class AuthenticationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class Authentication(BaseModel):
    api_key: str
    status: str = "authenticated"
