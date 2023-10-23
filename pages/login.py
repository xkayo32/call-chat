import nicegui
from decouple import config
from time import sleep


class LoginPage:

    def __init__(self, nicegui: nicegui) -> None:
        self.nicegui = nicegui
        self.ui = nicegui.ui

    def body(self):
        with self.ui.card().style('width: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'):
            with self.ui.column().style('align-items: center; width: 100%;'):
                with self.ui.row():
                    self.ui.image(
                        'https://seeklogo.com/images/C/chatcoin-chat-logo-D655A30A39-seeklogo.com.png')
                    self.ui.label('Chat Call').style('font-size: 2em;')
                self.username = self.ui.input('Username').style(
                    'width: 75%; margin-bottom: 1em;')
                self.password = self.ui.input(
                    'Password', password=True, password_toggle_button=True).style('width: 75%; margin-bottom: 1em;')
                with self.ui.row().style('width: 75%; justify-content: flex-end;'):
                    self.ui.button('Login', icon='login', on_click=self.__login).style(
                        'margin-bottom: 1em;')

    def __login(self):
        if self.username.value == config('USERNAME_CHAT') and self.password.value == config('PASSWORD_CHAT'):
            self.ui.open('/home')
        else:
            self.ui.notify('Login failed', type='negative', position='top')
