from aiogram.fsm.storage.redis import RedisStorage
from config_reader import config


storage_fsm = RedisStorage.from_url(f"{config.redis_url.get_secret_value()}")
