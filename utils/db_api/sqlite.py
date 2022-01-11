import sqlite3

from aiogram import types


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        # connection.set_trace_callback(self.logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_users(self):
        sql = """CREATE TABLE Users (
              id            INTEGER       PRIMARY KEY AUTOINCREMENT
                                          NOT NULL,
              user_id       INTEGER       NOT NULL,
              user_fullname VARCHAR (255) NOT NULL,
              user_login    VARCHAR (255),
              city          VARCHAR (255) NOT NULL,
              timezone      INTEGER       NOT NULL,
              subscription  BOOLEAN       NOT NULL
                                          DEFAULT (TRUE) 
                );"""
        return self.execute(sql, commit=True)

    def add_user(self, user_id: int, user_fullname: str, user_login: str, timezone: int, city: str):
        sql = """INSERT INTO Users(user_id, user_fullname, user_login, city, timezone, subscription) VALUES(?, ?, ?, ?, ?, TRUE)"""
        parameters = (user_id, user_fullname, f'@{user_login}', city, timezone)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self, **kwargs):
        if kwargs:
            sql = """SELECT * FROM Users WHERE """
            sql, parameters = self.formatted_args(sql, kwargs)
            return self.execute(sql, parameters, fetchall=True)
        sql = """SELECT * FROM Users"""
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = """SELECT * FROM Users WHERE """
        sql, parameters = self.formatted_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def change_city(self, parameters: tuple):
        sql = """UPDATE Users SET city=?, timezone=? WHERE user_id=?"""
        self.execute(sql, parameters=parameters, commit=True)

    def change_subscription(self, parameters: tuple):
        sql = """UPDATE Users SET subscription=? WHERE user_id=?"""
        self.execute(sql, parameters=parameters, commit=True)

    def update_fullname(self, parameters: tuple):
        sql = """UPDATE Users SET user_fullname=? WHERE user_id=?"""
        self.execute(sql, parameters=parameters, commit=True)

    def update_login(self, parameters: tuple):
        sql = """UPDATE Users SET user_login=? WHERE user_id=?"""
        self.execute(sql, parameters=parameters, commit=True)

    def check_validation(self, message: types.Message):
        current_user = self.select_user(user_id=message.from_user.id)
        if current_user is None:
            return False
        if current_user[2] != message.from_user.full_name:
            self.update_fullname((message.from_user.full_name, message.from_user.id))
        if current_user[3] != f'@{message.from_user.username}':
            self.update_login((f'@{message.from_user.username}', message.from_user.id))

    @staticmethod
    def formatted_args(sql, parameters: dict):
        sql += " AND ".join([f"{item}=?" for item in parameters])
        return sql, tuple(parameters.values())

    @staticmethod
    def logger(statement):
        print(f"""
    __________________________________________
    Executing:
    {statement}
    __________________________________________
    """)
