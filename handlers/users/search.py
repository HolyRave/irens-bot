from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import bot_start
from keyboards.default.doc_buttons import head_buttons
from keyboards.default.drive_buttons import sites_dct, down_level
from loader import dp
from states.searching import Search
from utils.google_api.gdocs import content_by_header


@dp.message_handler(lambda message: message.text in sites_dct.keys(), state=Search.first_lvl)
async def fstlvl(message: types.Message, state: FSMContext):
    if message.text in sites_dct.keys():
        underbt, underdict = down_level(sites_dct, message.text)
    else:
        bback = (await state.get_data())['back2']
        underbt, underdict = down_level(bback, message.text.strip())
    await message.answer(f"Нашли!", reply_markup=underbt)
    await Search.second_lvl.set()
    await state.update_data(files=underdict, platform=message, backfold=message)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Search.second_lvl)
async def scndlvl(message: types.Message, state: FSMContext):
    if message.text != '/start':
        platform = (await state.get_data())['platform']
        if message.text.strip() in ['Меню']:
            await state.finish()
            await bot_start(message, state)
        elif message.text.strip() in ['Назад']:
            back = (await state.get_data())['backfold']
            if back.text == platform.text:
                await state.finish()
                await bot_start(message, state)
            else:
                await Search.first_lvl.set()
                await fstlvl(platform, state)
        else:
            file_dct = (await state.get_data())['files']
            file_dct = {key.strip(): value for key, value in file_dct.items()}
            if 'application/vnd.google-apps.folder' in file_dct.get(message.text.strip(), ''):
                file_dct = {key.strip(): value[0].strip() for key, value in file_dct.items()}
                lvl2bt, lvl2dct = down_level(file_dct, message.text.strip())
                await message.answer(f'Файл {message.text.strip()} найден!', reply_markup=lvl2bt)
                await state.update_data(files=lvl2dct, backfold=message, back2=file_dct)
            else:
                file_dct = {key.strip(): value[0] for key, value in file_dct.items()}
                hed, site_bt, cont = head_buttons(file_dct.get(message.text.strip(), ''))
                await message.answer(f'Документ {message.text.strip()} найден!', reply_markup=site_bt)
                await Search.past.set()
                await state.update_data(header=hed, elem=cont)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Search.past)
async def pst(message: types.Message, state: FSMContext):
    if message.text.strip() != '/start':
        if message.text.strip() in ['Меню']:
            await state.finish()
            await bot_start(message, state)
        elif message.text.strip() in ['Назад']:
            to_doc = (await state.get_data())['backfold']
            await Search.first_lvl.set()
            await fstlvl(to_doc, state)
        else:
            header = (await state.get_data())['header']
            header = {key.strip(): value for key, value in header.items()}
            elem = (await state.get_data())['elem']
            await message.answer(content_by_header(elem, header[message.text.strip()]))
