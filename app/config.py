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
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    ELASTIC_PORT: str
    
    WEB_DOMAIN: str
    WEB_PORT: str
    
    model_config = SettingsConfigDict(env_file=".env", extra='allow')
    
    def get_web_url(self):
        return f'{self.WEB_DOMAIN}:{self.WEB_PORT}'

settings = Settings()

    