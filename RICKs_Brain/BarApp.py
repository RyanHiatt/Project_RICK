import json
import time
import pandas as pd

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
from kivy.uix.spinner import Spinner

# ----------------------------------------------------------------------------------------------------------------------
#   Project: R.I.C.K.
#   Description: Radically Intelligent Cocktail Kiosk
#   Version: 0.2.0
#   Created By: Ryan Hiatt
#   Date Started: 11/17/2020
# ----------------------------------------------------------------------------------------------------------------------

# TODO DrinkDB
# TODO Exception Handling! (Try, Except) Google kivy exception handling
# TODO Clean up imports

# Current Version of Kivy
kivy.require('2.0.0')

# Window Configuration
Window.size = (800, 480)
# Window.fullscreen = True

PASS_KEY = '8093'


class LoginScreen(Screen):
    # TODO Add graphics to left and right of keypad
    # TODO Determine pass through variables for top left of home screen
    # TODO Finalize design
    # TODO Check description, usage, and structure

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
        self.nope_label.text = ''

    # Runs when submit button is pressed, checks for correct key
    def submit(self):
        if LoginScreen.current_key == PASS_KEY:
            self.ids.passkey.text = ''
            LoginScreen.current_key = ''
            self.manager.current = 'home'

        # If the key is incorrect, the else statement runs
        else:
            self.ids.passkey.text = ''
            LoginScreen.current_key = ''

            self.nope_label.text = 'Invalid Pass Key!'


class HomeScreen(Screen):
    # TODO Beautify layout
    # TODO Determine top left component
    # TODO Finalize layout and design
    # TODO Check description, usage, and structure

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

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Kivy schedule update_clock callback once every second
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, dt):
        # Get the current time
        now = time.time()

        # Set the time Criteria
        local_time = time.localtime(now)
        time_format = '%H:%M:%S'
        time_stamp = time.strftime(time_format, local_time)

        # Update the time on the home screen
        self.clock_label.text = time_stamp

    def open_lockpop(self):
        # TODO Finalize design
        # TODO Finalize Layout

        # Initiate Popup
        pop = Popup(size_hint=(0.6, 0.6),
                    auto_dismiss=False,
                    title='R.I.C.K.',
                    title_align='center',
                    title_size=40)

        # Main Grid
        main_grid = GridLayout(rows=2)
        pop.add_widget(main_grid)

        # Row 1
        label1 = Label(text='Sign Out?\nWill Require Passkey Next Use',
                       text_size=self.size,
                       font_size=30,
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

        # Add Grid 2 to Main Grid
        main_grid.add_widget(btn_grid)

        # Open the Popup
        pop.open()

    # If Yes ('Sign Out') is clicked this function sets the screen to login screen
    def exit_pop(self, *args):
        self.manager.current = 'login'


class AllDrinksScreen(Screen):
    # TODO Update description, usage, and structure
    # TODO Finalize Layout
    # TODO Finalize Design
    # TODO Possibly change categories button to filter button

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

    # Sets up the size of child widget to be scrollable and initiates building of child widgets
    def setup_scrollview(self, dt):
        self.drink_layout.bind(minimum_height=self.drink_layout.setter('height'))

        self.create_drink_btns()

    # Creates a drink layout with button, label, and all respective properties for each drink in DrinkDB
    def create_drink_btns(self):
        # Opens DrinkDB file
        with open('../Dataframe/DrinkDB.json', 'r') as file:
            drink_db = json.load(file)

        # Iterates through each drink
        for i in range(len(drink_db['drinks'])):
            # Creates the path to each image
            img_path = '../Images/DrinkDB_Images/{}'.format(drink_db['drinks'][i]['img'])

            # Unit GridLayout
            btn_unit = GridLayout(rows=2,
                                  size_hint_y=None,
                                  size_hint_x=None,
                                  height=190,
                                  width=210)

            # Button/Image
            btn_unit.add_widget(Button(text=drink_db['drinks'][i]['name'],
                                       color=[0, 0, 0, 0],
                                       background_normal=img_path,
                                       size_hint_y=None,
                                       size_hint_x=None,
                                       height=160,
                                       width=210,
                                       on_release=self.btn_press))

            # Name Label
            btn_unit.add_widget(Label(text=drink_db['drinks'][i]['name'],
                                      font_size=20,
                                      halign='center',
                                      valign='bottom',
                                      size_hint_y=None,
                                      size_hint_x=None,
                                      height=30,
                                      width=210))

            # Create layout
            self.drink_layout.add_widget(btn_unit)

    # On the press of any drink button do this
    def btn_press(self, instance):

        global selected_drink
        selected_drink = instance.text

        self.manager.current = 'dispense'


class DispenseScreen(Screen):
    # TODO Add option to add drink to favorites list
    # TODO Fill out description, usage, and structure
    # TODO Convert to more dynamic screen able to work for all drinks, shots, and create drink
    # TODO Finalize design

    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    # This method tells the screen to update its parameters upon entering
    def on_enter(self, *args):

        Clock.schedule_once(self.setup_dispense_screen)

    def setup_dispense_screen(self, dt):
        with open('../Dataframe/DrinkDB.json', 'r') as file:
            drink_db = json.load(file)

        for i in range(len(drink_db['drinks'])):

            if drink_db['drinks'][i]['name'] == selected_drink:
                drink_profile = drink_db['drinks'][i]

                self.name_label.text = drink_profile['name']

                self.garnish_label.text = drink_profile['garnish']

                self.instructions_label.text = drink_profile['instructions']

                img_path = '../Images/DrinkDB_Images/{}'.format(drink_profile['img'])
                self.drink_img.source = img_path

                self.ingredient_layout.clear_widgets()

                for ingredient, amount in drink_profile['ingredients'].items():

                    self.ingredient_layout.add_widget(Label(text=str(ingredient),
                                                            font_size=20,
                                                            size_hint_y=None,
                                                            height=30))

                    self.ingredient_layout.add_widget(Label(text=str(amount) + ' OZ',
                                                            font_size=20,
                                                            size_hint_y=None,
                                                            height=30))


class FilterScreen(Screen):
    # TODO Fill out description, usage, and structure
    # TODO Search by letter?
    # TODO Create new design layout (user friendly, and modern)
    # TODO Define button press

    """
    -- Description --


    -- Usage --


    -- Structure --

    """


class SelectShotsScreen(Screen):
    # TODO Redesign lower portion
    # TODO New images, no background or black background?
    # TODO Does this lead into a popup or into a shots 'all drinks screen'?
    # TODO Fill out description, usage, and structure

    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    def btn_press(self):
        print('ok')


class DisplayShotsScreen(Screen):
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class FavoritesScreen(Screen):
    # TODO Determine how to add and remove favorites from some sort of list
    # TODO Fill out description, usage, and structure
    # TODO Finalize layout
    # TODO Finalize Design
    # TODO Screen Label

    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    favorites_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FavoritesScreen, self).__init__(**kwargs)

        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.favorites_layout.bind(minimum_height=self.favorites_layout.setter('height'))
        self.create_drink_btns()

    def create_drink_btns(self):
        with open('../Dataframe/DrinkDB.json', 'r') as file:
            drink_db = json.load(file)

        for i in range(len(drink_db['drinks'])):
            img_path = '../Images/DrinkDB_Images/{}'.format(drink_db['drinks'][i]['img'])

            btn_unit = GridLayout(rows=2,
                                  size_hint_y=None,
                                  size_hint_x=None,
                                  height=190,
                                  width=210)

            btn_unit.add_widget(Button(background_normal=img_path,
                                       size_hint_y=None,
                                       size_hint_x=None,
                                       height=160,
                                       width=210,
                                       on_release=self.btn_press))

            btn_unit.add_widget(Label(text=drink_db['drinks'][i]['name'],
                                      font_size=20,
                                      halign='center',
                                      valign='bottom',
                                      size_hint_y=None,
                                      size_hint_x=None,
                                      height=30,
                                      width=210))

            self.favorites_layout.add_widget(btn_unit)

    # On the press of any drink button do this
    def btn_press(self, instance):
        global selected_drink
        selected_drink = instance.text

        self.manager.current = 'dispense'


class CreateDrinkScreen(Screen):
    # TODO Fill out description, usage, and structure
    # TODO Layout possibly with pictures, simplified and modern
    # TODO Finalize Layout
    # TODO Finalize Design
    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    def __init__(self, **kwargs):
        super(CreateDrinkScreen, self).__init__(**kwargs)

        Clock.schedule_once(self.setup_custom_drink_screen, 1)

    def setup_custom_drink_screen(self, dt):

        on_hand = pd.read_csv('../Dataframe/OnHand.csv')
        on_hand = on_hand.sort_values(by='Name', ascending=True)

        spinner_values = []
        for i in on_hand.index:
            spinner_values.append(on_hand.loc[i, 'Name'])

        # Create 5 spinners for ingredient selection
        for i in range(1, 6):

            # Create Spinner with all active on-hand ingredients
            self.custom_drink_layout.add_widget(Spinner(text='None',
                                                        values=tuple(spinner_values),
                                                        size_hint=(None, None),
                                                        width=500,
                                                        height=50))

            # Spacer Label
            self.custom_drink_layout.add_widget(Label())

            # Create Spinner with
            self.custom_drink_layout.add_widget(Spinner(text='Amount',
                                                        values=('0.25', '0.5', '0.75', '1',
                                                                '1.25', '1.5', '1.75', '2',
                                                                '2.25', '2.5', '2.75', '3',
                                                                '3.25', '3.5', '3.75', '4',
                                                                '4.25', '4.5', '4.75', '5'),
                                                        size_hint=(None, None),
                                                        width=100,
                                                        height=50))

            self.custom_drink_layout.add_widget(Label(text='OZ',
                                                      font_size=20,
                                                      size_hint=(None, None),
                                                      width=50,
                                                      height=50))

            self.custom_drink_layout.add_widget(Label(size_hint=(None, None),
                                                      width=25,
                                                      height=50))


class MyScreenManager(ScreenManager):
    # TODO check description, and structure, add additional info
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
                   FilterScreen(name='filter'),
                   SelectShotsScreen(name='shots'),
                   DisplayShotsScreen(name='select_shot'),
                   FavoritesScreen(name='favorites'),
                   CreateDrinkScreen(name='create')]

        for screen in screens:
            self.add_widget(screen)


class BarApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    BarApp().run()
