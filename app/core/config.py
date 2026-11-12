from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Mobile Banking API - Kenya"
    version: str = "1.0.0"
    max_dti_ratio: float = 0.4  # CBK guideline 40%
    min_approval_ratio: float = 1.5

settings = Settings()
