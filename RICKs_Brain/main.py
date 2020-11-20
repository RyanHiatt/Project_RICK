import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# ----------------------------------------------------------------------------------------------------------------------
#   Project: RICK
#   Description: Radically Intelligent Cocktail Kiosk
#   Version: 0.2.0
#   Created By: Ryan Hiatt
#   Date Started: 11/17/2020
# ----------------------------------------------------------------------------------------------------------------------

# Current Version of Kivy
kivy.require('1.11.1')

# Window Configuration
Window.size = (800, 480)
# Window.fullscreen = True


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    def open_lockpop(self):
        """
        STRUCTURE
        Popup:
            GridLayout:
                Label:
                GridLayout:
                    AnchorLayout:
                        Button:
                    AnchorLayout:
                        Button:
        :return:
        """
        pop = Popup(size_hint=(0.5, 0.5),
                    auto_dismiss=False,
                    title='Sign Out',
                    title_align='center',
                    title_size=30)
        grid1 = GridLayout(rows=2)
        label1 = Label(text='Sign Out?',
                       text_size=self.size,
                       font_size=50,
                       halign='center',
                       valign='middle')
        grid2 = GridLayout(size_hint_y=0.33,
                           cols=2)
        anchor1 = AnchorLayout(anchor_x='left',
                               anchor_y='bottom')
        btn1 = Button(width=100,
                      height=60,
                      text='NO',
                      font_size=20)
        btn1.bind(on_release=pop.dismiss)
        anchor2 = AnchorLayout(anchor_x='right',
                               anchor_y='bottom')
        btn2 = Button(width=100,
                      height=60,
                      text='YES',
                      font_size=20)
        btn2.bind(on_release=self.exit_pop)
        btn2.bind(on_release=pop.dismiss)

        anchor1.add_widget(btn1)
        anchor2.add_widget(btn2)
        grid2.add_widget(anchor1)
        grid2.add_widget(anchor2)
        grid1.add_widget(label1)
        grid1.add_widget(grid2)
        pop.add_widget(grid1)
        pop.open()

    def exit_pop(self, *args):
        self.manager.current = 'login'


class AllDrinksScreen(Screen):
    pass


class CategoriesScreen(Screen):
    pass


class ShotsScreen(Screen):
    pass


class CreateDrinkScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


class BarApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        screenlist = [LoginScreen(name='login'),
                      HomeScreen(name='home'),
                      AllDrinksScreen(name='drinks'),
                      CategoriesScreen(name='category'),
                      ShotsScreen(name='shots'),
                      CreateDrinkScreen(name='create')]

        sm = MyScreenManager()
        for i in screenlist:
            sm.add_widget(i)
        return sm


if __name__ == '__main__':
    BarApp().run()
