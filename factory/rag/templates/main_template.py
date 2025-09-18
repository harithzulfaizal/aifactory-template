MAIN_TEMPLATE = """
from fastapi import FastAPI
from rag_config import RAGConfig

app = FastAPI()

# Load configuration
config = RAGConfig.from_yaml("config.yaml")

@app.get("/")
def read_root():
    return {"message": "RAG Template API", "config": config.dict()}
"""
