import nicegui
from decouple import config
from time import sleep
from database.query import DataBase


class HomePage(DataBase):

    def __init__(self, nicegui: nicegui) -> None:
        super().__init__()
        self.nicegui = nicegui
        self.ui = nicegui.ui
        self.messages = list()

    def body(self):
        self.name = False
        self.messages.append(('Bem vindo ao chat', 'Chat Call'))
        self.messages.append(('Digite seu nome de usuário', 'Chat Call'))
        with self.ui.right_drawer(bordered=True, elevated=True).style('display: flex;flex-direction: column;'):
            with self.ui.column():
                with self.ui.element('div').style('flex: 1;overflow-y: auto;'):
                    self.ui.button('Resetar').on(
                        'click', self.__reset_chat)
                with self.ui.element('div'):
                    self.chat_box()
                with self.ui.element('div').style('bottom: 0;position: absolute; margin-bottom: 10px;'):
                    with self.ui.row():
                        self.username = self.ui.input(
                            autocomplete=False, placeholder='Eu me chamo...')
                        self.username.props('rounded outlined dense')
                        self.username.on('keydown.enter', self.__save_username)
                        self.message = self.ui.textarea()
                        self.message.visible = False
                        self.message.props('rounded outlined dense')
                        self.message.on('keydown.enter', self.__send_message)
                        self.btn_send = self.ui.button(icon='send')
                        self.btn_send.on('click', self.__save_username)

        with self.ui.element('div').style('display: flex;flex-direction: column;'):
            with self.ui.tabs().classes('w-full') as tabs:
                tab_clientes = self.ui.tab('Clientes')
                tab_planos = self.ui.tab('Planos')
                tab_faturas = self.ui.tab('Faturas')

            with self.ui.tab_panels(tabs, value=tab_clientes).style('flex: 1;'):
                with self.ui.tab_panel(name=tab_clientes):
                    self.__clientes()
                with self.ui.tab_panel(name=tab_planos):
                    self.__planos()
                with self.ui.tab_panel(name=tab_faturas):
                    self.__faturas()

    def __save_username(self, event):
        if self.name is False:
            if any([self.username.value.lower().strip() == item[1].lower().strip() for item in self.rows_clients]):
                self.name = self.username.value
                self.messages = list()
                self.messages.append((f'Bem vindo {self.name}', 'Chat Call'))
                self.messages.append(('Qual sua dúvida?', 'Chat Call'))
                self.username.visible = False
                self.message.visible = True
                self.btn_send.on('click', self.__send_message)
            else:
                self.messages.append(
                    ('Usuário não encontrado, tente novamente', 'Chat Call'))
                self.username.value = ''
            self.chat_box.refresh()

    def __send_message(self, event):
        if self.name is not False:
            self.messages.append((self.message.value, self.name))
            self.message.value = ''
            self.chat_box.refresh()

    def __clientes(self):
        self.rows_clients = self.select('clientes', '*')
        rows = [{'nome': row[1], 'email': row[2], 'telefone': row[3], 'endereco': row[4], 'plano_id': row[5]}
                for row in self.rows_clients]
        self.ui.table(
            columns=[
                {'name': 'nome', 'label': 'Nome', 'field': 'nome'},
                {'name': 'email', 'label': 'Email', 'field': 'email'},
                {'name': 'telefone', 'label': 'Telefone', 'field': 'telefone'},
                {'name': 'endereco', 'label': 'Endereço', 'field': 'endereco'},
                {'name': 'plano_id', 'label': 'Plano', 'field': 'plano_id'},
            ], rows=rows)

    def __planos(self):
        self.rows_planos = self.select('planos', '*')
        rows = [{'nome': row[1], 'valor': row[2]} for row in self.rows_planos]
        self.ui.table(
            columns=[
                {'name': 'nome', 'label': 'Nome', 'field': 'nome'},
                {'name': 'valor', 'label': 'Valor', 'field': 'valor'},
            ], rows=rows)

    def __faturas(self):
        self.rows_faturas = self.select('faturas', '*')
        rows = [{'cliente_id': row[1], 'valor': row[2], 'data_vencimento': row[3],
                 'data_pagamento': row[4], 'pago': row[5]} for row in self.rows_faturas]
        self.ui.table(
            columns=[
                {'name': 'cliente_id', 'label': 'Cliente', 'field': 'cliente_id'},
                {'name': 'valor', 'label': 'Valor', 'field': 'valor'},
                {'name': 'data_vencimento', 'label': 'Data de Vencimento',
                    'field': 'data_vencimento'},
                {'name': 'data_pagamento', 'label': 'Data de Pagamento',
                    'field': 'data_pagamento'},
                {'name': 'pago', 'label': 'Pago', 'field': 'pago'},
            ], rows=rows)

    def __reset_chat(self):
        self.messages = list()
        self.messages.append(('Bem vindo ao chat', 'Chat Call'))
        self.messages.append(('Digite seu nome de usuário', 'Chat Call'))
        self.chat_box.refresh()
        self.username.visible = True
        self.username.value = ''
        self.message.visible = False
        self.name = False

    @nicegui.ui.refreshable
    def chat_box(self):
        for text, user in self.messages:
            self.ui.chat_message(text=text, name=user)
