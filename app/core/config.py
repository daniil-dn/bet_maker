from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, PostgresDsn, model_validator, field_validator
from pydantic_settings import BaseSettings

load_dotenv('.env')
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """SERVER CONFIG"""
    DEBUG: Optional[bool] = True

    REDIS_PORT: int = None
    REDIS_HOST: str = None

    @model_validator(mode='before')
    @classmethod
    def model_validator(cls, values: Any) -> Any:
        if not values.get('DEBUG'):
            values['DEBUG'] = False
        cls.assemble_armq_url(values)
        cls.assemble_logger_level(values)
        cls.assemble_logger_path(values)
        cls.assemble_db_connection(values)
        return values

    API_V1_STR: str = "/api/v1"

    # 60 minutes * 24 hours * 8 days = 8 days
    SERVER_NAME: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_LOGIN: str
    RABBITMQ_PASSWORD: str
    ARMQ_URL: str = None

    @classmethod
    def assemble_armq_url(cls, values: Dict[str, Any]):
        if isinstance(values.get("ARMQ_URL"), str):
            return

        host = values.get("RABBITMQ_HOST")
        port = values.get("RABBITMQ_PORT")
        login = values.get("RABBITMQ_LOGIN")
        password = values.get("RABBITMQ_PASSWORD")

        if all([host, port, login, password]):
            values["ARMQ_URL"] = f"amqp://{login}:{password}@{host}:{port}"
        else:
            values["ARMQ_URL"] = None

    SERVER_HOST: AnyHttpUrl

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    # PYTHONPATH
    PYTHONPATH: str

    # logger config
    LOGGER_PATH: Path = None
    LOGGER_ROTATION: str = "10 MB"
    LOGGER_COMPRESSION: str = "zip"
    LOGGER_DEBUG: bool = False
    LOGGER_LEVELS: list = []

    @classmethod
    def assemble_logger_level(cls, values: Dict[str, Any]) -> Any:
        debug_lvl = values.get("LOGGER_DEBUG")

        if debug_lvl is True:
            values["LOGGER_LEVELS"] = ["INFO", "DEBUG", "ERROR"]
        else:
            values["LOGGER_LEVELS"] = ["INFO", "ERROR"]

    @classmethod
    def assemble_logger_path(cls, values: Dict[str, Any]) -> Any:

        python_path = values.get("PYTHONPATH")

        if python_path:
            values['LOGGER_PATH'] = Path(python_path).resolve() / 'app' / 'logs'

        else:
            values['LOGGER_PATH'] = BASE_DIR / 'logs'

    """DATABASE CONFIG"""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_SYNC_URI: Optional[PostgresDsn] = None

    @classmethod
    def assemble_db_connection(cls, values: Dict[str, Any]) -> Any:
        if isinstance(values.get("SQLALCHEMY_DATABASE_URI"), str):
            return
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB")

        if all([user, password, host, db]):
            values["SQLALCHEMY_DATABASE_URI"] = f"postgresql+asyncpg://{user}:{password}@{host}/{db}"
        else:
            values["SQLALCHEMY_DATABASE_URI"] = None

    class ConfigDict:
        case_sensitive = True


settings = Settings()
