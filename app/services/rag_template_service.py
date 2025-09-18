from app.schemas.rag_models import RAGConfig
from factory.rag.rag_templater import generate_rag_template


class RAGTemplateService:
    @staticmethod
    def generate_template(config: RAGConfig) -> str:
        return generate_rag_template(config)
