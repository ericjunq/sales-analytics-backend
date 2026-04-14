from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str 
    secret_key: str 
    access_token_expires_minutes: int 
    refresh_token_expires_days: int 
    algorithm: str
    ai_api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()