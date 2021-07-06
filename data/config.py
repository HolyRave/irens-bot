from environs import Env
from utils.google_api.creds import main, user_parse
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str


def admins():
    str_admins = main()
    ADMINS = []  # Тут у нас будет список из админов
    for admin in str_admins:
        try:
            ADMINS.append(int(admin))
        except Exception as e:
            pass
    return ADMINS


def users():
    str_users = user_parse()
    USERS = []  # Тут у нас будет список белого листа
    for admin in str_users:
        try:
            USERS.append(int(admin))
        except Exception as e:
            pass
    return USERS

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста


