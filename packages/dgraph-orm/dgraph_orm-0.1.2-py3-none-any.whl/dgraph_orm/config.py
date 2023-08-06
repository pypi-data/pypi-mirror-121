from pydantic import BaseSettings
from pathlib import Path

import os

ENV = os.environ.get("ENV", "live")


class Settings(BaseSettings):
    dgraph_url: str
    dgraph_access_token: str

    class Config:
        env_file = Path(__file__).parent.parent / f".env.{ENV}"


settings = Settings()
