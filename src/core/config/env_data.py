from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV(BaseSettings):
    # Database
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str

    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "extra": "ignore",
    }


Config = ENV()
