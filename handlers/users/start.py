from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from keyboards.default.drive_buttons import site_res, sites_dct, down_level
from loader import dp
from states.searching import Search
from data import config


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    with open('data/startlog.txt', 'r', encoding='utf-8') as f:
        startset = set(line for line in f)
        startset \
            .add(
            f'- id:{message.from_user.id}, name:{message.from_user.full_name}, username:@{message.from_user.username}\n')
    with open('data/startlog.txt','w', encoding='utf-8') as f:
        for line in list(startset):
            f.write(line)

    if message.from_user.id in config.ADMINS:
        btn, _ = site_res(True)
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=btn)
    else:
        btn, _ = site_res()
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=btn)
    await Search.first_lvl.set()
