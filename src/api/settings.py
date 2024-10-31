from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_expire: int

    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str

    class Config:
        env_file = ".env"


settings = Settings()
