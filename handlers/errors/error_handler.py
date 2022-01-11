import logging

import emoji

from loader import dp

# Create a logging instance
logger = logging.getLogger('error_handler')

# Assign a file-handler to that instance
fh = logging.FileHandler("errors.txt")

# Format your logs (optional)
formatter = logging.Formatter('\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)  # This will set the format to the file handler

# Add the handler to your logging instance
logger.addHandler(fh)


def emoji_fix(string):
    return emoji.demojize(string, delimiters=(":", ":"))


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest)

    if isinstance(exception, CantDemoteChatCreator):
        logger.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logger.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logger.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logger.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logger.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logger.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logger.exception(f'InvalidQueryID: {exception} \nUpdate: {emoji_fix(str(update))}')
        return True

    if isinstance(exception, TelegramAPIError):
        logger.exception(f'TelegramAPIError: {exception} \nUpdate: {emoji_fix(str(update))}')
        return True

    if isinstance(exception, RetryAfter):
        logger.exception(f'RetryAfter: {exception} \nUpdate: {emoji_fix(str(update))}')
        return True

    if isinstance(exception, CantParseEntities):
        logger.exception(f'CantParseEntities: {exception} \nUpdate: {emoji_fix(str(update))}')
        return True

    if isinstance(exception, BadRequest):
        logger.exception(f'CantParseEntities: {exception} \nUpdate: {emoji_fix(str(update))}')
        return True

    logger.exception(f'Update: {emoji_fix(str(update))} \n{exception}')
