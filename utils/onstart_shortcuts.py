from aiogram import Dispatcher, types
from utils.google_api.shortcut import parse_documents


async def on_startup_commands(dp: Dispatcher):
    """
    Set commands to a bot
    :param dp:
    :return:
    """
    data = parse_documents()
    commands = [types.BotCommand(command=k.strip().replace(' ','_'), description=w[0][0:100]) for k, w in data.items()]

    await dp.bot.set_my_commands(commands)
