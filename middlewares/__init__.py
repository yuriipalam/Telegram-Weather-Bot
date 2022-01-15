from aiogram import Dispatcher

from .check_validation import CheckValidation
from .check_handler import CheckHandler
from .log import HandlersLogger
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware(1))
    dp.middleware.setup(CheckValidation())
    dp.middleware.setup(HandlersLogger())
    dp.middleware.setup(CheckHandler())
