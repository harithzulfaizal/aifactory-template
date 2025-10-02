import os
import uuid

from jinja2 import Environment, FileSystemLoader

from app.schemas.rag_models import RAGConfig


def generate_rag_template(config: RAGConfig) -> str:
    folder_name = f"rag_template_{uuid.uuid4().hex[:8]}"
    folder_path = os.path.join(os.path.dirname(__file__), "output", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Create directory structure
    directories = ["ingestion", "vector_db", "retrieval", "utils"]

    for directory in directories:
        os.makedirs(os.path.join(folder_path, directory), exist_ok=True)

    # Setup Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))

    # Render templates using .j2 files
    config_content = env.get_template("config.j2").render(**config.model_dump())
    requirements_content = env.get_template("requirements.txt.j2").render()
    main_content = env.get_template("main.py.j2").render()
    config_py_content = env.get_template("config.py.j2").render()

    # Core files
    with open(os.path.join(folder_path, "config.yaml"), "w") as f:
        f.write(config_content)

    with open(os.path.join(folder_path, "requirements.txt"), "w") as f:
        f.write(requirements_content)

    with open(os.path.join(folder_path, "main.py"), "w") as f:
        f.write(main_content)

    with open(os.path.join(folder_path, "config.py"), "w") as f:
        f.write(config_py_content)

    # __init__.py files
    init_content = env.get_template("init.py.j2").render()

    with open(os.path.join(folder_path, "__init__.py"), "w") as f:
        f.write(init_content)

    with open(os.path.join(folder_path, "ingestion", "__init__.py"), "w") as f:
        f.write(init_content)

    with open(os.path.join(folder_path, "vector_db", "__init__.py"), "w") as f:
        f.write(init_content)

    with open(os.path.join(folder_path, "retrieval", "__init__.py"), "w") as f:
        f.write(init_content)

    with open(os.path.join(folder_path, "utils", "__init__.py"), "w") as f:
        f.write(init_content)

    # Ingestion module
    upload_handler_content = env.get_template("upload_handler.py.j2").render()
    with open(os.path.join(folder_path, "ingestion", "upload_handler.py"), "w") as f:
        f.write(upload_handler_content)

    sharepoint_handler_content = env.get_template("sharepoint_handler.py.j2").render()
    with open(
        os.path.join(folder_path, "ingestion", "sharepoint_handler.py"), "w"
    ) as f:
        f.write(sharepoint_handler_content)

    document_processor_content = env.get_template("document_processor.py.j2").render()
    with open(
        os.path.join(folder_path, "ingestion", "document_processor.py"), "w"
    ) as f:
        f.write(document_processor_content)

    # Utils module
    text_splitter_content = env.get_template("text_splitter.py.j2").render()
    with open(os.path.join(folder_path, "utils", "text_splitter.py"), "w") as f:
        f.write(text_splitter_content)

    embeddings_content = env.get_template("embeddings.py.j2").render()
    with open(os.path.join(folder_path, "utils", "embeddings.py"), "w") as f:
        f.write(embeddings_content)

    # Vector DB module
    vector_db_base_content = env.get_template("vector_db_base.py.j2").render()
    with open(os.path.join(folder_path, "vector_db", "base.py"), "w") as f:
        f.write(vector_db_base_content)

    azure_search_content = env.get_template("azure_search.py.j2").render()
    with open(os.path.join(folder_path, "vector_db", "azure_search.py"), "w") as f:
        f.write(azure_search_content)

    chroma_db_content = env.get_template("chroma_db.py.j2").render()
    with open(os.path.join(folder_path, "vector_db", "chroma_db.py"), "w") as f:
        f.write(chroma_db_content)

    vector_db_factory_content = env.get_template("vector_db_factory.py.j2").render()
    with open(os.path.join(folder_path, "vector_db", "factory.py"), "w") as f:
        f.write(vector_db_factory_content)

    # Retrieval module
    semantic_search_content = env.get_template("semantic_search.py.j2").render()
    with open(os.path.join(folder_path, "retrieval", "semantic_search.py"), "w") as f:
        f.write(semantic_search_content)

    # Create .env.example file
    env_example_content = env.get_template(".env_example.j2").render(config=config)
    with open(os.path.join(folder_path, ".env.example"), "w") as f:
        f.write(env_example_content)

    # Create Dockerfile
    dockerfile_content = env.get_template("dockerfile.j2").render()
    with open(os.path.join(folder_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # Create README.md
    readme_content = env.get_template("readme.md.j2").render(config=config)
    with open(os.path.join(folder_path, "README.md"), "w") as f:
        f.write(readme_content)

    return folder_path
