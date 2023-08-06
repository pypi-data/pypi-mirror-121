from pydantic import BaseSettings

class Settings(BaseSettings):
    kibela_team: str = "my"
    kibela_access_token: str = "ACCESS_TOKEN"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
