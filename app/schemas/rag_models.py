from pydantic import BaseModel, Field
from typing import Optional, List

from typing import Dict, Any


class ChunkingConfig(BaseModel):
    method: str = Field(..., description="Chunking method: fixed, semantic, hybrid")
    chunk_size: int = Field(..., description="Number of tokens/characters per chunk")
    overlap: int = Field(0, description="Number of overlapping tokens between chunks")


class MetadataConfig(BaseModel):
    include: List[str] = Field(
        default_factory=list,
        description="Metadata fields to include: file_name, file_type, page_number, etc.",
    )


class EmbeddingConfig(BaseModel):
    model: str = Field(
        ..., description="Embedding model name (e.g., text-embedding-ada-002)"
    )
    dimension: Optional[int] = Field(
        None, description="Vector dimension (needed for some DBs)"
    )


class IngestionConfig(BaseModel):
    source_type: str = Field(..., description="Data source: local, cloud, api, db")
    file_types: List[str] = Field(
        ..., description="Supported file types (pdf, docx, etc.)"
    )
    recursive: bool = Field(False, description="Recursively load files")
    encoding: str = Field("utf-8", description="File encoding")
    chunking: ChunkingConfig
    metadata: MetadataConfig
    embeddings: EmbeddingConfig


class VectorDBConfig(BaseModel):
    type: str = Field(
        ..., description="Vector DB type (pinecone, weaviate, azure_search, etc.)"
    )
    uri: Optional[str] = Field(None, description="Connection string / URI")
    index_name: str = Field(..., description="Index/collection name")
    distance_metric: str = Field(
        "cosine", description="Similarity metric: cosine, dot_product, euclidean"
    )
    dynamic_fields: Optional[bool] = Field(
        False, description="Enable dynamic schema (JSON schema/programmatic)"
    )


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
