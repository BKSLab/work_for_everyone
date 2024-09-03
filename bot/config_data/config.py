from dataclasses import dataclass
from pathlib import Path

from aiogram.fsm.storage.redis import RedisStorage
from database.redis import redis
from environs import Env


@dataclass
class TgBotConfig:
    token: str
    storage: RedisStorage


@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    name: str


@dataclass
class AppConfig:
    admin_user_id: int
    access_token_hh: str
    base_dir: Path


@dataclass
class Config:
    tg_bot: TgBotConfig
    db: DbConfig
    app: AppConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    tg_bot_config = TgBotConfig(
        token=env.str('TOKEN'),
        storage=RedisStorage(redis=redis)
    )

    db_config = DbConfig(
        host=env.str('DB_HOST'),
        user=env.str('POSTGRES_USER'),
        password=env.str('POSTGRES_PASSWORD'),
        name=env.str('DB_NAME')
    )

    app_config = AppConfig(
        admin_user_id=env.int('USER_ID_ADMIN'),
        access_token_hh=env.str('ACCESS_TOKEN'),
        base_dir=Path(__file__).resolve(strict=True).parent.parent
    )

    return Config(
        tg_bot=tg_bot_config,
        db=db_config,
        app=app_config
    )
