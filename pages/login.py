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
                self.ui.label('Login').style('font-size: 2em;')
                self.username = self.ui.input('Username').style(
                    'width: 75%; margin-bottom: 1em;')
                self.password = self.ui.input(
                    'Password', password=True, password_toggle_button=True).style('width: 75%; margin-bottom: 1em;')
                with self.ui.row().style('width: 75%; justify-content: flex-end;'):
                    self.ui.button('Login', icon='login', on_click=self.__login).style(
                        'margin-bottom: 1em;')

    def __login(self):
        print(self.username.value, self.password.value)
        if self.username.value == config('USERNAME_CHAT') and self.password.value == config('PASSWORD_CHAT'):
            self.ui.notify('Login successful', type='positive', position='top')
            sleep(0.5)
            self.ui.open('/home')
        else:
            self.ui.notify('Login failed', type='negative', position='top')
