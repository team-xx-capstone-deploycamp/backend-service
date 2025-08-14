from typing import List, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    app_name: str = "FastAPI ML API"
    allow_origins: List[str] = Field(default=["*"])

    # Basic Auth
    basic_auth_username: str = "admin"
    basic_auth_password: str = "changeme"

    # Model
    model_path: str = "model/used_car_price_model_v2.pkl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )

    @field_validator('allow_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            # Try to parse as JSON
            try:
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                # If JSON parsing fails, handle as comma-separated string
                return [origin.strip() for origin in v.split(",")]
        return v if v is not None else ["*"]

settings = Settings()
