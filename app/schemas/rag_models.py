from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class DocumentSourceType(str, Enum):
    UPLOAD = "upload"
    SHAREPOINT = "sharepoint"
    BOTH = "both"


class FieldType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    LIST = "list"


class MetadataField(BaseModel):
    name: str = Field(..., description="Field name")
    type: FieldType = Field(..., description="Field data type")
    description: Optional[str] = Field(None, description="Field description")
    auto_extract: bool = Field(False, description="Auto-extract from document")
    extract_prompt_template: Optional[str] | None = Field(
        None, description="Custom prompt template for extraction"
    )
    default_value: Optional[Any] = Field(None, description="Default value if not found")
    required: bool = Field(False, description="Whether this field is required")


class ChunkingConfig(BaseModel):
    method: Literal["fixed", "semantic", "hybrid"] = Field(
        ..., description="Chunking method"
    )
    chunk_size: int = Field(..., description="Number of tokens/characters per chunk")
    overlap: int = Field(0, description="Number of overlapping tokens between chunks")


class MetadataConfig(BaseModel):
    fields: List[MetadataField] = Field(
        default_factory=lambda: [
            MetadataField(
                name="title",
                type=FieldType.STRING,
                auto_extract=False,
                description="Document title",
                default_value=None,
                required=True,
                extract_prompt_template=None,
            ),
            MetadataField(
                name="page",
                type=FieldType.INTEGER,
                auto_extract=False,
                description="Page number",
                default_value=None,
                required=False,
                extract_prompt_template=None,
            ),
            MetadataField(
                name="content",
                type=FieldType.STRING,
                auto_extract=False,
                description="Document content",
                default_value=None,
                required=True,
                extract_prompt_template=None,
            ),
            MetadataField(
                name="content_vector",
                type=FieldType.LIST,
                auto_extract=False,
                description="Content vector embeddings",
                default_value=None,
                required=True,
                extract_prompt_template=None,
            ),
        ],
        description="Metadata fields schema",
    )


class LLMConfig(BaseModel):
    model: str = Field(..., description="Azure OpenAI large language model name")


class EmbeddingConfig(BaseModel):
    model: str = Field(..., description="Azure OpenAI embedding model name")


class SharePointConfig(BaseModel):
    site_url: str = Field(..., description="SharePoint site URL")
    tenant_id: str = Field(..., description="Azure AD tenant ID")
    client_id: str = Field(..., description="Azure AD app client ID")
    client_secret: str = Field(..., description="Azure AD app client secret")
    folder_path: Optional[str] = Field(
        None, description="Specific folder path (optional)"
    )
    recursive: bool = Field(True, description="Recursively process subfolders")


class IngestionConfig(BaseModel):
    source_type: DocumentSourceType = Field(..., description="Document source type")
    sharepoint: Optional[SharePointConfig] = Field(
        None, description="SharePoint configuration"
    )
    chunking: ChunkingConfig
    metadata: MetadataConfig
    embeddings: EmbeddingConfig


class VectorDBConfig(BaseModel):
    type: Literal["azure_search"] = Field("azure_search", description="Vector DB type")
    index_name: str = Field(..., description="Index/collection name")
    distance_metric: Literal["cosine", "dot_product", "euclidean"] = Field(
        "cosine", description="Similarity metric"
    )


class QueryConfig(BaseModel):
    retrieval_type: str = Field(
        "semantic", description="Retrieval method: semantic, hybrid, keyword"
    )
    top_k: int = Field(5, description="Number of documents to return")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Metadata filters (e.g. {file_type: pdf})"
    )
    reranker: bool = Field(
        False, description="Enable reranker (bm25, cross-encoder, etc.)"
    )
    context_window: Optional[int] = Field(
        2048, description="Max tokens per query context"
    )


class RAGConfig(BaseModel):
    ingestion: IngestionConfig
    vector_db: VectorDBConfig
    query: QueryConfig
