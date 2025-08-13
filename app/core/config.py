from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

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

settings = Settings()
