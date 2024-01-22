from dataclasses import dataclass
from pathlib import Path

from aiogram.fsm.storage.redis import RedisStorage
from database.redis import redis

# from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env


@dataclass
class TgBot:
    token: str
    storage: RedisStorage


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('TOKEN'), storage=RedisStorage(redis=redis))
    )
    # return Config(tg_bot=TgBot(token=env('TOKEN'), storage=MemoryStorage()))


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
