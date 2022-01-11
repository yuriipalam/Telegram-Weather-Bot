from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

help_buttons_off_sub = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Сменить город",
                                                                         callback_data="change_city")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Отключить рассылку погоды",
                                                                         callback_data="off_sub")
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Закрыть меню",
                                                                         callback_data="close_menu")
                                                ]
                                            ])

help_buttons_on_sub = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="Сменить город",
                                                                        callback_data="change_city")
                                               ],
                                               [
                                                   InlineKeyboardButton(text="Включить рассылку погоды",
                                                                        callback_data="on_sub")
                                               ],
                                               [
                                                   InlineKeyboardButton(text="Закрыть меню",
                                                                        callback_data="close_menu")
                                               ]
                                           ])
