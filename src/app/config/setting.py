import os
from functools import lru_cache

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    PROFILE: str
    APP_NAME: str = "YIT"
    LOG_LEVEL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 4
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_PASS: str
    SMTP_SENDER_NAME: str

    HOST: str = '0.0.0.0'
    PORT: int = 9508
    UVICORN_RELOAD: bool = True

    API_V1_PREFIX: str = '/api/v1'
    TITLE: str = 'imc'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'institution management system APIs'
    DOCS_URL: str | None = f'{API_V1_PREFIX}/docs'
    REDOCS_URL: str | None = f'{API_V1_PREFIX}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_PREFIX}/openapi'
    IMAGES_PATH: str

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str

    # SSL_KEYFILE: str
    # SSL_CERTFILE: str

    MIDDLEWARE_CORS: bool = True

    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    FILE_LOC: str

    # db
    DATABASE_URL: str

    # cors
    CORS_ORIGIN: list[str]

    #UI
    UI_RESET_LINK: str
    UI_LOGIN_LINK: str

    #supportMail
    SUPPORT_EMAIL: str

    #organizationName
    ORGANIZATION_NAME: str = 'Young Innovators Academy'



# make an entry here if you are creating new env
config = dict(
    dev='src/resource/env/dev.env',

)




@lru_cache
def get_setting() -> Settings:
    return Settings(_env_file=("src/resource/env/.env", config[os.environ.get('ENV', 'dev').lower()]))
