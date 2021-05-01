from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.rethinkdb import RethinkDBStorage
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RethinkDBStorage(db=config.DB_creds.get('db_name'), table='aiogram', user=config.DB_creds.get('username'),
                           password=config.DB_creds.get('password'), host=config.DB_creds.get('host'),
                           port=int(config.DB_creds.get('port')))
dp = Dispatcher(bot, storage=storage)
