from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.drive_buttons import site_res, sites_dct, down_level
from loader import dp
from states.searching import Search
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    btn, _ = site_res()
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=btn)
    await Search.first_lvl.set()
