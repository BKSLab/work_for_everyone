from aiogram.fsm.storage.redis import Redis
from environs import Env

env = Env()
env.read_env()
redis = Redis(
    host='localhost',
    port=6379,
    password=env('PASSWORD_REDIS'),
    decode_responses=True,
)
