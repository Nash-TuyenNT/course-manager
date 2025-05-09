from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    GOOGLE_API_KEY: str
    GOOGLE_EMBEDDINGS_MODEL: str
    SERPAPI_API_KEY: str

    @property
    def sqlalchemy_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    @property
    def google_api_key(self):
        return self.GOOGLE_API_KEY

    @property
    def google_embeddings_model(self):
        return self.GOOGLE_EMBEDDINGS_MODEL

    @property
    def serpapi_api_key(self):
        return self.SERPAPI_API_KEY

    class Config:
        env_file = ".env"


settings = Settings()
