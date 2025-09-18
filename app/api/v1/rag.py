from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
import zipfile
import os

from app.schemas.rag_models import RAGConfig
from app.services.rag_template_service import RAGTemplateService
from app.core.logging import get_logger

rag_router = APIRouter()
logger = get_logger("rag")


@rag_router.post("/generate_template")
async def generate_rag_template(request: RAGConfig):
    logger.info("Received request to generate RAG template")
    logger.info(f"Request data: {request.model_dump()}")
    folder_to_zip = RAGTemplateService.generate_template(request)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_to_zip)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)

    logger.info("Zip file created")
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=rag_template.zip"},
    )
