import os
from typing import Optional, Dict, Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # 1. 定义字段和默认值（如果环境变量没搜到，就用这些）
    default_model: str = "deepseek-chat"
    default_provider: str = "deepseek"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    debug: bool = False
    log_level: str = "INFO"
    max_history_length: int = 100

    model_config = SettingsConfigDict(
        env_prefix="", env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
