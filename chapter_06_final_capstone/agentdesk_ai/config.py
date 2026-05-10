import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "AgentDesk AI Final Capstone"
    model: str = os.getenv("MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    remote_mcp_url: str = os.getenv("REMOTE_MCP_URL", "http://127.0.0.1:3010/mcp")
    kb_path: Path = BASE_DIR / "data" / "company_knowledge_base.json"


settings = Settings()

