import os

from fastapi import Header
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.schemas.auth_models import AuthenticationException


def check_authentication_header(X_PolicyGPT_Key: str = Header(None)):
    """Check if the provided API key is valid."""
    if X_PolicyGPT_Key == os.getenv("X_POLICYGPT_KEY"):
        return "Successful authorization"
    else:
        if X_PolicyGPT_Key is None or X_PolicyGPT_Key == "":
            raise AuthenticationException(
                "API request failed: No API key provided. Please include a valid API key."
            )
        else:
            raise AuthenticationException(
                "API request failed: Unauthorized access. Please check your API key."
            )


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle API key authentication for all API routes."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            api_key = request.headers.get("X-PolicyGPT-Key")
            if not api_key or api_key != os.getenv("X_POLICYGPT_KEY"):
                return JSONResponse(
                    status_code=401,
                    content={
                        "statusCode": 401,
                        "data": {
                            "answer": "",
                            "sources": "",
                        },
                        "isError": 1,
                        "errorMessage": "Unauthorized access. Please check your API key.",
                    },
                )
        return await call_next(request)
