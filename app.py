import sqlite3


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from handlers.admins.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from loader import db
    try:
        db.create_table_users()
    except sqlite3.OperationalError as err:
        print(err)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    from loader import loop
    from handlers.users.weather_auto_sender import weather_auto_sender
    try:
        loop.create_task(weather_auto_sender())
    except sqlite3.OperationalError:
        print('DataBase has not been setup yet')

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
