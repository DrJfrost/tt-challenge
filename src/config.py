from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    DATABASE_URL: str
    API_KEY: str
    ENVIRONMENT: str = "development"
    
    @property
    def is_prod(self) -> bool:
        return self.ENVIRONMENT == "production"

settings = Settings()