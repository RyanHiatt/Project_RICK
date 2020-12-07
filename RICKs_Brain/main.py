import kivy
from kivy.clock import Clock
from kivy.properties import ObjectProperty
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

PASS_KEY = '8093'


class LoginScreen(Screen):
    """
    -- Description --
    This screen contains a keypad and a text input. The user will have to input the correct sequence of numerical
    values and press submit to access the rest of the app. There is also a clear button and an error message popup
    for clearing wrong inputs and warning users that they input the wrong sequence respectively.

    -- Usage --
    Access Bar Application

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

    current_key = ''

    # Runs every time a numerical button is pressed
    def btn_press(self, instance):
        LoginScreen.current_key += str(instance.text)
        self.ids.passkey.text = self.ids.passkey.text + '*'

    # Runs when clear button is pressed (clears input)
    def clear_text(self):
        self.ids.passkey.text = ''
        LoginScreen.current_key = ''

    # Runs when submit button is pressed, checks for correct key
    def submit(self):
        if LoginScreen.current_key == PASS_KEY:
            self.ids.passkey.text = ''
            LoginScreen.current_key = ''
            self.manager.current = 'home'

        else:
            self.ids.passkey.text = ''
            LoginScreen.current_key = ''

            # Creates Incorrect Passkey Popup
            popup = Popup(title='Incorrect Passkey',
                          title_align='center',
                          size_hint=(0.5, 0.5),
                          auto_dismiss=False)

            # Popup Layout
            pop_layout = GridLayout(rows=2)

            # Popup Label
            nope_label = Label(text='Incorrect Passkey\n Please Try Again',
                               font_size=40)
            pop_layout.add_widget(nope_label)

            # Popup Close Button
            close_btn = Button(text='Close',
                               size_hint_y=0.4)
            close_btn.bind(on_release=popup.dismiss)
            pop_layout.add_widget(close_btn)

            # Add Layout to Popup
            popup.add_widget(pop_layout)

            # Open Popup
            popup.open()


class HomeScreen(Screen):
    """
    -- Description --
    The home screen as it implies is the central navigation hub of the whole application. From here users can navigate
    through the rest of the application through the use of button or log out back to the login screen.

    -- Usage --
    Access All Drinks Screen
    Access Shots Screen
    Access Favorites Screen
    Access Create Drink Screen
    Access Settings Screen
    Revert to Login Screen

    -- Structure --
    GridLayout:
        GridLayout:
            Label:
            Label:
            Label:
        GridLayout:
            AnchorLayout:
                Button:
            AnchorLayout:
                Button:
            AnchorLayout:
                Button:
            AnchorLayout:
                Button:
        GridLayout:
            AnchorLayout:
                Button:
            Label:
            AnchorLayout:
                Button:
    """

    def open_lockpop(self):

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
    This screen contains all the drinks available in the bar app. They will be organized alphabetically and displayed in
    a scrolling manor. The user can either go back to the home screen, select a drink, or select the categories button
    to be brought to the Categories Screen in which drinks are broken down into categories.

    -- Usage --
    Access Categories Screen
    Dispense Drink
    Revert to Home Screen

    -- Structure --
    GridLayout:
        ScrollView:
            GridLayout:
                Button (Dynamic):
        GridLayout:
            AnchorLayout:
                Button:
            Label:
            AnchorLayout:
                Button:
    """

    drink_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AllDrinksScreen, self).__init__(**kwargs)

        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.drink_layout.bind(minimum_height=self.drink_layout.setter('height'))
        self.create_drink_btns()

    def create_drink_btns(self):
        for i in range(100):
            self.drink_layout.add_widget(Button(text='Button {}'.format(i+1),
                                                size_hint_y=None,
                                                size_hint_x=None,
                                                height=180,
                                                width=220))


class DispenseScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class CategoriesScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class ShotsScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class FavoritesScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class CreateDrinkScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class MyScreenManager(ScreenManager):
    """
    -- Description --
    This object manages all the screens for the application as well as screen transitions.

    -- Structure --
    LoginScreen:
        HomeScreen:
            AllDrinksScreen:
                DispenseScreen:
                CategoriesScreen:
            ShotsScreen:
                DispenseScreen:
            FavoritesScreen:
                DispenseScreen:
            CreateDrinkScreen:
    """

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        screens = [LoginScreen(name='login'),
                   HomeScreen(name='home'),
                   AllDrinksScreen(name='drinks'),
                   DispenseScreen(name='dispense'),
                   CategoriesScreen(name='category'),
                   ShotsScreen(name='shots'),
                   FavoritesScreen(name='favorites'),
                   CreateDrinkScreen(name='create')]

        for screen in screens:
            self.add_widget(screen)


class BarApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    BarApp().run()
