from aiogram.fsm.storage.redis import Redis
from environs import Env

env = Env()
env.read_env()
redis = Redis(
    host=env('HOST'),
    password=env('PASSWORD_REDIS'),
    decode_responses=True,
)
