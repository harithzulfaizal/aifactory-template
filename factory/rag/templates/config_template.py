CONFIG_TEMPLATE = """
# RAG Configuration
ingestion:
  source_type: {{ ingestion.source_type }}
  file_types: {{ ingestion.file_types | tojson }}
  recursive: {{ ingestion.recursive }}
  encoding: {{ ingestion.encoding }}
  chunking:
    method: {{ ingestion.chunking.method }}
    chunk_size: {{ ingestion.chunking.chunk_size }}
    overlap: {{ ingestion.chunking.overlap }}
  metadata:
    include: {{ ingestion.metadata.include | tojson }}
  embeddings:
    model: {{ ingestion.embeddings.model }}
    dimension: {{ ingestion.embeddings.dimension }}

vector_db:
  type: {{ vector_db.type }}
  uri: {{ vector_db.uri }}
  index_name: {{ vector_db.index_name }}
  distance_metric: {{ vector_db.distance_metric }}
  dynamic_fields: {{ vector_db.dynamic_fields }}

query:
  retrieval_type: {{ query.retrieval_type }}
  top_k: {{ query.top_k }}
  filters: {{ query.filters | tojson if query.filters else None }}
  reranker: {{ query.reranker }}
  prompt_template: {{ query.prompt_template }}
  context_window: {{ query.context_window }}
  answer_style: {{ query.answer_style }}

{% if extraction %}
extraction:
  schema: {{ extraction.schema | tojson }}
  granularity: {{ extraction.granularity }}
  output_format: {{ extraction.output_format }}
{% endif %}

orchestration:
  llm_provider: {{ orchestration.llm_provider }}
  llm_model: {{ orchestration.llm_model }}
  temperature: {{ orchestration.temperature }}
  max_tokens: {{ orchestration.max_tokens }}
  api_key: {{ orchestration.api_key }}
"""
