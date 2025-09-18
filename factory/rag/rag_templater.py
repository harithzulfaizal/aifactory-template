import os
import uuid
from jinja2 import Template

from app.schemas.rag_models import RAGConfig
from factory.rag.templates.config_template import CONFIG_TEMPLATE
from factory.rag.templates.requirements_template import REQUIREMENTS_TEMPLATE
from factory.rag.templates.main_template import MAIN_TEMPLATE


def generate_rag_template(config: RAGConfig) -> str:
    folder_name = f"rag_template_{uuid.uuid4().hex[:8]}"
    folder_path = os.path.join(os.path.dirname(__file__), "output", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    config_content = Template(CONFIG_TEMPLATE).render(config.model_dump())
    requirements_content = Template(REQUIREMENTS_TEMPLATE).render(config.model_dump())
    main_content = Template(MAIN_TEMPLATE).render()

    with open(os.path.join(folder_path, "config.yaml"), "w") as f:
        f.write(config_content)

    with open(os.path.join(folder_path, "requirements.txt"), "w") as f:
        f.write(requirements_content)

    with open(os.path.join(folder_path, "main.py"), "w") as f:
        f.write(main_content)

    return folder_path
