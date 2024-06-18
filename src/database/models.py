import asyncio
import platform

from dotenv import load_dotenv

from pathlib import Path

from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
load_dotenv()


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    HOST: str
    PORT: int

    POSTGRES_URL: PostgresDsn

    #  JWT
    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ACCESS_EXP_TIME: int
    JWT_REFRESH_EXP_TIME: int
    JWT_ACCESS_ALGORITHM: str
    JWT_REFRESH_ALGORITHM: str

    #  GOOGLE_AUTH
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: HttpUrl


settings = Settings()

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async_engine = create_async_engine(
    url=settings.POSTGRES_URL.unicode_string(),
    pool_size=50,
    max_overflow=50,
)
async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

GOOGLE_AUTH_URL = (
    f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}"
    f"&redirect_uri={settings.GOOGLE_REDIRECT_URI.unicode_string()}&scope=openid%20profile%20email&access_type=offline"
)