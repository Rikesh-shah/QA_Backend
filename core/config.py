from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Setting(BaseSettings):
    DB_HOST :str
    DB_PASSWORD :str
    DB_USER : str
    SECRET_KEY : str
    SECRET_ALGORITHM : str
    TOKEN_EXPIRY_DAYS : int

    class Config:
        env_file = ".env"


settings = Setting()