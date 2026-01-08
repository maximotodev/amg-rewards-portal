from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This tells Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra="ignore")

    # Default values if not found in .env
    APP_NAME: str = "AMG Rewards Portal"
    DATABASE_URL: str = "mysql+pymysql://amg:amgpass@localhost:3306/amg_rewards"
    CORS_ORIGINS: list[str] = ["http://localhost:4200"]

settings = Settings()
