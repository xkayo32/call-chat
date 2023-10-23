import sqlite3
from faker import Faker
from datetime import datetime, timedelta


class DataBase:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('database/database.db')
        self.cursor = self.connection.cursor()

    def create_table(self, table_name: str, columns: list) -> None:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    def insert(self, table_name: str, columns: list, values: list) -> None:
        self.cursor.execute(
            f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        self.connection.commit()

    def select(self, table_name: str, columns: list, where: str = None) -> list:
        if where:
            self.cursor.execute(
                f'SELECT {columns} FROM {table_name} WHERE {where}')
        else:
            self.cursor.execute(f'SELECT {columns} FROM {table_name}')
        return self.cursor.fetchall()

    def update(self, table_name: str, columns: list, values: list, where: str = None) -> None:
        if where:
            self.cursor.execute(
                f'UPDATE {table_name} SET {columns} = {values} WHERE {where}')
        else:
            self.cursor.execute(
                f'UPDATE {table_name} SET {columns} = {values}')
        self.connection.commit()

    def delete(self, table_name: str, where: str = None) -> None:
        if where:
            self.cursor.execute(f'DELETE FROM {table_name} WHERE {where}')
        else:
            self.cursor.execute(f'DELETE FROM {table_name}')
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __del__(self) -> None:
        self.close()


# if __name__ == '__main__':
#     db = DataBase()
#     # Gerar tabelas
#     db.create_table(
#         'planos', 'id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, valor REAL')
#     db.create_table(
#         'clientes', 'id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, telefone TEXT, endereco TEXT, plano_id INTEGER')
#     db.create_table(
#         'faturas', 'id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, valor REAL, data_vencimento TEXT, data_pagamento TEXT, pago INTEGER')
#     db.create_table(
#         'ordem_servicos', 'id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, descricao TEXT, data TEXT, status TEXT')

#     # Gerar planos
#     db.insert('planos', 'nome, valor', '"Plano 1", 100.00')
#     db.insert('planos', 'nome, valor', '"Plano 2", 200.00')
#     db.insert('planos', 'nome, valor', '"Plano 3", 300.00')
#     db.insert('planos', 'nome, valor', '"Plano 4", 400.00')

#     fake = Faker()

#     # Gerar clientes
#     clientes = []
#     for i in range(30):
#         nome = fake.name()
#         email = fake.email()
#         telefone = fake.phone_number()
#         endereco = fake.address()
#         plano_id = fake.random_int(min=1, max=4)
#         clientes.append((nome, email, telefone, endereco, plano_id))

#     for cliente in clientes:
#         db.insert('clientes', 'nome, email, telefone, endereco, plano_id',
#                   f'"{cliente[0]}", "{cliente[1]}", "{cliente[2]}", "{cliente[3]}", {cliente[4]}')

#     from datetime import datetime, timedelta

# # Gerar faturas pagas
# faturas = []
# for i in range(30):
#     cliente_id = i + 1
#     data_vencimento = datetime.now() + timedelta(days=30)
#     data_pagamento = datetime.now() - timedelta(days=fake.random_int(min=1, max=30))
#     valor = fake.random_int(min=50, max=500)
#     faturas.append((cliente_id, data_vencimento, valor, data_pagamento))

# for fatura in faturas:
#     db.insert('faturas', 'cliente_id, data_vencimento, valor, data_pagamento, pago',
#               f'{fatura[0]}, "{fatura[1].strftime("%Y-%m-%d")}", {fatura[2]}, "{fatura[3].strftime("%Y-%m-%d")}", 1')

# faturas_vencidas = []
# for _ in range(10):
#     cliente_id = fake.random_int(min=1, max=30)
#     data_vencimento = datetime.now() - timedelta(days=fake.random_int(min=1, max=30))
#     data_pagamento = 'NULL'
#     valor = fake.random_int(min=50, max=500)
#     faturas_vencidas.append(
#         (cliente_id, data_vencimento, valor, data_pagamento))

# for fatura in faturas_vencidas:
#     db.insert('faturas', 'cliente_id, data_vencimento, valor, data_pagamento, pago',
#               f'{fatura[0]}, "{fatura[1].strftime("%Y-%m-%d")}", {fatura[2]}, {fatura[3]}, 0')

# # Gerar atendimentos
# atendimentos = []
# for i in range(30):
#     cliente_id = i + 1
#     data = datetime.now() - timedelta(days=fake.random_int(min=1, max=30))
#     descricao = fake.text()
#     atendimentos.append((cliente_id, data, descricao))
#     status = fake.random_element(elements=(0, 1))

# for atendimento in atendimentos:
#     db.insert('ordem_servicos', 'cliente_id, data, descricao, status',
#               f'{atendimento[0]}, "{atendimento[1].strftime("%Y-%m-%d")}", "{atendimento[2]}", {status}')
