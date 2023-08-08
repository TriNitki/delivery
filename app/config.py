from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # jwt config
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    
    # db config
    POSTGRES_URL: str
    CASSANDRA_KEYSPACE: str
    CASSANDRA_IP_ADDRESS: str
    ENDPOINT: str
    
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

settings = Settings()

    