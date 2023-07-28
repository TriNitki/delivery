from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # jwt config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # db config
    postgres_url: str
    cassandra_keyspace: str
    cassandra_ip_address: str
    endpoint: str
    
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

settings = Settings()

    