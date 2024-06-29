from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV(BaseSettings):
    # Database
    DATABASE_URL: str
    
    model_config: SettingsConfigDict = {
        'env_file': '.env',
        "extra": "ignore",
    }

Config = ENV()