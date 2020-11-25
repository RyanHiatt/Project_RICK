import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput

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
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        """
        -- Description --
        
        
        -- Structure --
        GridLayout:
            Label:
            GridLayout:
                Label:
                TextInput:
                GridLayout:
                    Button(x12):
                Label:
            Label:
        """

        # Main Grid
        main_grid = GridLayout(cols=3)

        # Left Column
        label1 = Label()
        main_grid.add_widget(label1)

        # Center Column
        center_grid = GridLayout(rows=4)
        label3 = Label(size_hint_y=0.1)
        center_grid.add_widget(label3)

        # Row 1
        text = TextInput(size_hint_y=0.2)
        center_grid.add_widget(text)

        # Row 2
        key_grid = GridLayout(cols=3, rows=4)
        center_grid.add_widget(key_grid)

        # Key Grid
        for i in range(1, 10):
            btn = Button(text=str(i),
                         font_size=80,
                         id='btn' + str(i),
                         on_release=self.btn_press)
            key_grid.add_widget(btn)

        key_grid.add_widget(Button(text='Clear',
                                   font_size=50,
                                   id='clear',
                                   on_release=self.btn_press))
        key_grid.add_widget(Button(text='0',
                                   font_size=80,
                                   id='btn0',
                                   on_release=self.btn_press))
        key_grid.add_widget(Button(text='Submit',
                                   font_size=50,
                                   id='submit',
                                   on_release=self.submit))

        # Row 3
        label4 = Label(size_hint_y=0.1)
        center_grid.add_widget(label4)

        # Add Center Grid to Main Grid
        main_grid.add_widget(center_grid)

        # Right Column
        label2 = Label()
        main_grid.add_widget(label2)

        # Load Screen
        self.add_widget(main_grid)

    def btn_press(self, instance):
        pass

    def clear_values(self):
        pass

    def submit(self, *args):
        self.manager.current = 'home'


class HomeScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    def open_lockpop(self):
        """
        -- Description --


        -- Structure --
        Popup:
            GridLayout:
                Label:
                GridLayout:
                    AnchorLayout:
                        Button:
                    AnchorLayout:
                        Button:
        """

        # Initiate Popup
        pop = Popup(size_hint=(0.5, 0.5),
                    auto_dismiss=False,
                    title='Sign Out',
                    title_align='center',
                    title_size=30)

        # Main Grid
        main_grid = GridLayout(rows=2)
        pop.add_widget(main_grid)

        # Row 1
        label1 = Label(text='Sign Out?',
                       text_size=self.size,
                       font_size=50,
                       halign='center',
                       valign='middle')
        main_grid.add_widget(label1)

        # Row 2
        btn_grid = GridLayout(size_hint_y=0.33,
                           cols=2)

        # No Button
        anchor1 = AnchorLayout(anchor_x='left',
                               anchor_y='bottom')
        btn1 = Button(width=100,
                      height=60,
                      text='NO',
                      font_size=20,
                      on_release=pop.dismiss)
        anchor1.add_widget(btn1)
        btn_grid.add_widget(anchor1)

        # Yes Button
        anchor2 = AnchorLayout(anchor_x='right',
                               anchor_y='bottom')
        btn2 = Button(width=100,
                      height=60,
                      text='YES',
                      font_size=20,
                      on_press=pop.dismiss)
        btn2.bind(on_release=self.exit_pop)
        btn2.bind(on_release=pop.dismiss)
        anchor2.add_widget(btn2)
        btn_grid.add_widget(anchor2)

        # Add Grid 2 to Grid
        main_grid.add_widget(btn_grid)

        # Open the Popup
        pop.open()

    def exit_pop(self, *args):
        self.manager.current = 'login'


class AllDrinksScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    pass


class CategoriesScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    pass


class ShotsScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    pass


class FavoritesScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    pass


class CreateDrinkScreen(Screen):
    """
    -- Description --


    -- Structure --

    """

    pass


class MyScreenManager(ScreenManager):
    """
    -- Description --


    -- Structure --

    """

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        screens = [LoginScreen(name='login'),
                   HomeScreen(name='home'),
                   AllDrinksScreen(name='drinks'),
                   CategoriesScreen(name='category'),
                   ShotsScreen(name='shots'),
                   CreateDrinkScreen(name='create')]

        for screen in screens:
            self.add_widget(screen)


class BarApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    BarApp().run()
