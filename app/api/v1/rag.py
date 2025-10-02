import io
import json
import os
import zipfile
from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from app.core.logging import get_logger
from app.schemas.rag_models import RAGConfig
from app.services.rag_template_service import RAGTemplateService

rag_router = APIRouter()
logger = get_logger("rag")


@rag_router.post("/generate_template")
async def generate_rag_template(
    config: str = Form(...), files: Optional[List[UploadFile]] = File(None)
):
    """
    Generate RAG template with optional file uploads.

    - config: JSON string containing RAG configuration
    - files: Optional list of files to include when source_type is 'upload' or 'both'
    """
    logger.info("Received request to generate RAG template")

    try:
        print(config)
        config_dict = json.loads(config)
        rag_config = RAGConfig(**config_dict)

        logger.info(f"Configuration parsed: {rag_config.model_dump()}")
        logger.info(f"Files received: {len(files) if files else 0}")

        # Validate file requirements
        if rag_config.ingestion.source_type in ["upload", "both"] and not files:
            raise ValueError(
                "Files are required when source_type is 'upload' or 'both'"
            )

        if rag_config.ingestion.source_type == "sharepoint" and files:
            logger.warning(
                "Files provided but source_type is 'sharepoint' - files will be ignored"
            )

        # Generate template
        folder_to_zip = RAGTemplateService.generate_template(rag_config)

        # Add uploaded files to the template if applicable
        if files and rag_config.ingestion.source_type in ["upload", "both"]:
            samples_dir = os.path.join(folder_to_zip, "sample_documents")
            os.makedirs(samples_dir, exist_ok=True)

            for file in files:
                if file.filename:
                    file_path = os.path.join(samples_dir, file.filename)
                    content = await file.read()
                    with open(file_path, "wb") as f:
                        f.write(content)
                    logger.info(f"Added sample file: {file.filename}")

        # Create zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(folder_to_zip):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_to_zip)
                    zip_file.write(file_path, arcname)
        zip_buffer.seek(0)

        logger.info("Zip file created successfully")

        # Clean up the temporary folder
        import shutil

        shutil.rmtree(folder_to_zip, ignore_errors=True)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=rag_template.zip"},
        )

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config: {str(e)}")
        raise ValueError(f"Invalid configuration JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        raise ValueError(f"Template generation failed: {str(e)}")
