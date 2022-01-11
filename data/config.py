import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
WEATHER_TOKENS = str(os.getenv("WEATHER_TOKENS")).split(',')
SERVER_TIMEZONE = int(os.getenv("SERVER_TIMEZONE"))

admins = [
    877287293
]
