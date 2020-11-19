import kivy

# Current Version of Kivy
kivy.require('1.11.1')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import Settings


# ----------------------------------------------------------------------------------------------------------------------
#   Project: RICK
#   Description: Radically Intelligent Cocktail Kiosk
#   Version: 0.2.0
#   Created By: Ryan Hiatt
#   Date Started: 11/17/2020
# ----------------------------------------------------------------------------------------------------------------------

# Window Configuration
Window.size = (800, 480)
# Window.fullscreen = True


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


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
