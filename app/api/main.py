from fastapi import APIRouter

from app.api.deps import AuthMiddleware
from app.api.v1 import rag

api_router = APIRouter()

api_router.include_router(rag, prefix="/v1/rag", tags=["rag"])

__all__ = ["api_router", "AuthMiddleware"]
