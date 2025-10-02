from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class DocumentSourceType(str, Enum):
    UPLOAD = "upload"
    SHAREPOINT = "sharepoint"
    LOCAL = "local"


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
                auto_extract=True,
                description="Document title",
                default_value=None,
                required=False,
            ),
            MetadataField(
                name="page",
                type=FieldType.INTEGER,
                auto_extract=True,
                description="Page number",
                default_value=None,
                required=False,
            ),
            MetadataField(
                name="content",
                type=FieldType.STRING,
                auto_extract=True,
                description="Document content",
                default_value=None,
                required=True,
            ),
            MetadataField(
                name="content_vector",
                type=FieldType.LIST,
                auto_extract=False,
                description="Content vector embeddings",
                default_value=None,
                required=False,
            ),
        ],
        description="Metadata fields schema",
    )


class EmbeddingConfig(BaseModel):
    model: str = Field(..., description="Azure OpenAI embedding model name")
    dimension: Optional[int] = Field(
        None, description="Vector dimension (auto-detected for Azure OpenAI)"
    )
    azure_endpoint: Optional[str] = Field(None, description="Azure OpenAI endpoint")
    api_version: str = Field(
        "2024-02-15-preview", description="Azure OpenAI API version"
    )


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
    file_types: List[str] = Field(
        default=["pdf", "docx", "txt", "png", "jpeg"],
        description="Supported file types",
    )
    sharepoint: Optional[SharePointConfig] = Field(
        None, description="SharePoint configuration"
    )
    chunking: ChunkingConfig
    metadata: MetadataConfig
    embeddings: EmbeddingConfig


class AzureAISearchConfig(BaseModel):
    endpoint: str = Field(..., description="Azure AI Search endpoint")
    api_key: str = Field(..., description="Azure AI Search admin key")
    api_version: str = Field("2024-07-01", description="Azure AI Search API version")
    semantic_configuration: Optional[str] = Field(
        None, description="Semantic search configuration name"
    )


class ChromaDBConfig(BaseModel):
    persist_directory: Optional[str] = Field(
        "./chroma_db", description="Local storage directory"
    )
    host: Optional[str] = Field(None, description="Chroma server host")
    port: Optional[int] = Field(None, description="Chroma server port")
    ssl: bool = Field(False, description="Use SSL for remote connection")


class VectorDBConfig(BaseModel):
    type: Literal["azure_search", "chroma", "pinecone", "weaviate"] = Field(
        ..., description="Vector DB type"
    )
    index_name: str = Field(..., description="Index/collection name")
    distance_metric: Literal["cosine", "dot_product", "euclidean"] = Field(
        "cosine", description="Similarity metric"
    )
    dynamic_fields: bool = Field(
        False, description="Enable dynamic schema (JSON schema/programmatic)"
    )
    azure_search: Optional[AzureAISearchConfig] = Field(
        None, description="Azure AI Search configuration"
    )
    chroma: Optional[ChromaDBConfig] = Field(
        None, description="Chroma DB configuration"
    )
    uri: Optional[str] = Field(None, description="Legacy connection string / URI")


class QueryConfig(BaseModel):
    retrieval_type: str = Field(
        "semantic", description="Retrieval method: semantic, hybrid, keyword"
    )
    top_k: int = Field(5, description="Number of documents to return")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Metadata filters (e.g. {file_type: pdf})"
    )
    reranker: Optional[str] = Field(
        None, description="Reranker method (bm25, cross-encoder, etc.)"
    )
    prompt_template: Optional[str] = Field(
        None, description="Template for prompt injection"
    )
    context_window: Optional[int] = Field(
        2048, description="Max tokens per query context"
    )
    answer_style: Optional[str] = Field(
        "concise", description="Answer style: concise, detailed, JSON, etc."
    )


class ExtractionField(BaseModel):
    field: str
    type: str
    description: Optional[str] = None


class ExtractionConfig(BaseModel):
    schema: List[ExtractionField] = Field(
        default_factory=list, description="Schema definition for extracted fields"
    )
    granularity: str = Field(
        "document", description="Extraction level: page, chunk, document"
    )
    output_format: str = Field("json", description="Output format: json, csv, etc.")


class OrchestrationConfig(BaseModel):
    llm_provider: str = Field(
        ..., description="Provider: openai, azure_openai, anthropic, etc."
    )
    llm_model: str = Field(..., description="Model name (e.g., gpt-4, llama2-70b)")
    temperature: float = Field(0.0, description="Sampling temperature")
    max_tokens: int = Field(1024, description="Maximum tokens for completion")
    api_key: Optional[str] = Field(
        None, description="Reference to API key (can be env var)"
    )


class RAGConfig(BaseModel):
    ingestion: IngestionConfig
    vector_db: VectorDBConfig
    query: QueryConfig
    extraction: Optional[ExtractionConfig] = None
    orchestration: OrchestrationConfig
