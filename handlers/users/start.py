from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from keyboards.default.drive_buttons import site_res, sites_dct, down_level, void
from loader import dp
from states.searching import Search, Reg
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

    if message.from_user.id in config.admins():
        btn, _ = site_res(True)
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=btn)
        await Search.first_lvl.set()
    elif message.from_user.id in config.users():
        btn, _ = site_res()
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=btn)
        await Search.first_lvl.set()
    else:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             "Вы незарегистрированный пользователь!\n"
                             "Попросите вашего администратора вас зарегистрировать.", reply_markup=void)
        await Reg.unreg.set()


@dp.message_handler(state=Reg.unreg, content_types=types.ContentTypes.ANY)
async def unreg(message: types.Message):
    await message.answer("Вы незарегистрированный пользователь, повторите позже", reply_markup=void)
