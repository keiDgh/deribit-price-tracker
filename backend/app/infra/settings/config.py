from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    app_name: str
    
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    redis_port: str
    redis_host: str
    cache_ttl_seconds: int

    deribit_api_url: str
    collect_interval_seconds: int

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}"    

settings = Settings()