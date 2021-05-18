from aiogram import executor
from loader import dp
import middlewares, filters, handlers
from utils.onstart_shortcuts import on_startup_commands


async def on_startup(dp):
    # Уведомляет про запуск
    await on_startup_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
