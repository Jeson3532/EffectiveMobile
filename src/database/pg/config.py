from pydantic_settings import BaseSettings, SettingsConfigDict
import pyprojroot as ppr
from typing import Annotated

root_path = ppr.here()
env_path = root_path / '.env'


class DBConfig(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'postgres_db'
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(extra="ignore", env_file=env_path)

    @property
    def url(self) -> Annotated[str, "URL подключения к БД"]:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")
