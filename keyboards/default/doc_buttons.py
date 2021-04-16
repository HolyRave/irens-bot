from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.google_api.gdocs import get_headers, content_by_header


def head_buttons(document_id):
    hed, get_content = get_headers(document_id)
    headers = [x for x in hed.keys()]
    formatted_2d_list = [headers[x:x + 5] for x in range(0, len(headers), 5)]
    site_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6,
                                      keyboard=[[KeyboardButton(text=x) for x in itm]
                                                for itm in formatted_2d_list])
    site_button.row('Меню',"Назад")

    return hed, site_button, get_content
