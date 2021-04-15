from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.buttons import sites_dct, down_level
from loader import dp
from states.searching import Search


@dp.message_handler(lambda message: message.text in sites_dct.keys(), state=Search.first_lvl)
async def fstlvl(message: types.Message, state: FSMContext):
    underbt, underdict = down_level(sites_dct, message.text)
    await message.answer(f"Нашли!", reply_markup=underbt)
    await Search.second_lvl.set()
    await state.update_data(files=underdict)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Search.second_lvl)
async def scndlvl(message: types.Message, state: FSMContext):
    if message.text != '/start':
        all = (await state.get_data())['files']
        if 'application/vnd.google-apps.folder' in all.get(message.text):
            all = {key: value[0] for key, value in all.items()}
            lvl2bt, lvl2dct = down_level(all, message.text)
            await message.answer('Нашли!', reply_markup=lvl2bt)
            await state.update_data(files=lvl2dct)
        else:
            await message.answer("Тест")