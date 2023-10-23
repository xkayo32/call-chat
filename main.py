import nicegui
from pages.login import LoginPage
from pages.home import HomePage


@nicegui.ui.page('/home')
def page_home():
    HomePage(nicegui).body()


LoginPage(nicegui).body()

nicegui.ui.run(title='Chat Call')
