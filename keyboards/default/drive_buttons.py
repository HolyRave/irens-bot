from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.google_api.api_credentials import service


def get_root():
    result = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                  pageSize=10, fields="nextPageToken, files(id,name, parents)").execute()
    items = result.get('files', [])
    root = ''
    for item in items:
        parents = item.get('parents', [''])
        item['parents'] = parents[0]
        if item['parents'] == '':
            root = item['id']
    service.close()
    return root


def site_res():
    site_result = service.files().list(q=f'"{get_root()}" in parents',
                                       pageSize=10, fields="files(id,name, parents)").execute()
    sites = site_result.get('files', [])
    formatted_2d_list = [sites[x:x + 3] for x in range(0, len(sites), 3)]
    site_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3,
                                      keyboard=[[KeyboardButton(text=x['name']) for x in itm]
                                                for itm in formatted_2d_list])
    sites_dict = {site['name']: site['id'] for site in sites}
    service.close()
    return site_button, sites_dict


_, sites_dct = site_res()


def down_level(site: dict, site_name: str):
    new_result = service.files().list(q=f"'{site[f'{site_name}']}' in parents",
                                      pageSize=10, fields="nextPageToken, files(id,name, parents, mimeType)").execute()
    items = new_result.get('files', [])
    down_folder = {item['name']: [item['id'], item['mimeType']] for item in items}
    formatted_2d_list = [items[x:x + 3] for x in range(0, len(items), 3)]
    butt = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[[KeyboardButton(text=x['name']) for x in item]
                                         for item in formatted_2d_list])
    service.close()
    butt.row('Меню', "Назад")
    return butt, down_folder
