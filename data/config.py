from environs import Env
from utils.google_api.creds import main
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

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста


