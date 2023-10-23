from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# class DataBase:

#     def __init__(self) -> None:
#         self.connection = sqlite3.connect('database/database.db')
#         self.cursor = self.connection.cursor()

#     def create_table(self, table_name: str, columns: list) -> None:
#         self.cursor.execute(
#             f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

#     def insert(self, table_name: str, columns: list, values: list) -> None:
#         self.cursor.execute(
#             f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
#         self.connection.commit()

#     def select(self, table_name: str, columns: list, where: str = None) -> list:
#         if where:
#             self.cursor.execute(
#                 f'SELECT {columns} FROM {table_name} WHERE {where}')
#         else:
#             self.cursor.execute(f'SELECT {columns} FROM {table_name}')
#         return self.cursor.fetchall()

#     def update(self, table_name: str, columns: list, values: list, where: str = None) -> None:
#         if where:
#             self.cursor.execute(
#                 f'UPDATE {table_name} SET {columns} = {values} WHERE {where}')
#         else:
#             self.cursor.execute(
#                 f'UPDATE {table_name} SET {columns} = {values}')
#         self.connection.commit()

#     def delete(self, table_name: str, where: str = None) -> None:
#         if where:
#             self.cursor.execute(f'DELETE FROM {table_name} WHERE {where}')
#         else:
#             self.cursor.execute(f'DELETE FROM {table_name}')
#         self.connection.commit()

#     def close(self) -> None:
#         self.connection.close()

#     def __del__(self) -> None:
#         self.close()


class DataBase:
    def __init__(self) -> None:
        engine = create_engine('sqlite:///database/database.db')
        metadata = MetaData()
        metadata.reflect(bind=engine)
        self.session = Session(engine)
        self.base = automap_base()
        self.base.prepare(engine)

    def select_itens(self, table: str, where_column: str = None, where_value: str | int = None):
        Date = self.base.classes[table]
        if where_column and where_value:
            resultado = self.session.query(Date).filter(
                getattr(Date, where_column) == where_value).all()
        else:
            resultado = self.session.query(Date).all()
        return [item.__dict__ for item in resultado]
