from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.jsonshorts import get_params


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Похоже бот перезапустился!"
                         f"Напишите /start")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text in ['/'+x for x in list(get_params().keys())]:
        data = get_params()
        for item in data[message.text[1::]]:
            await message.answer(item)
    else:
        state = await state.get_state()
        await message.answer(f"Такого файла или документа нет на диске!")
