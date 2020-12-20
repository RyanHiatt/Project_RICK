import json
import time
import datetime
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
from kivy.uix.textinput import TextInput


# ----------------------------------------------------------------------------------------------------------------------
#   Project: RICK
#   Description: Radically Intelligent Cocktail Kiosk
#   Version: 0.2.0
#   Created By: Ryan Hiatt
#   Date Started: 11/17/2020
# ----------------------------------------------------------------------------------------------------------------------

# TODO DrinkDB
# TODO ShotsDB
# TODO Keep name R.I.C.K. or change?
# TODO Exception Handling! (Try, Except) Google kivy exception handling
# TODO Clean up imports

# Current Version of Kivy
kivy.require('1.11.1')

# Window Configuration
Window.size = (800, 480)
# Window.fullscreen = True

# TODO Configuration file?
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

        # Kivy schedule update_date callback only once to set date
        Clock.schedule_once(self.update_date, 1)

        # Kivy schedule interval to check for new date every hour
        Clock.schedule_interval(self.update_date, 3600)

    def update_clock(self, dt):
        # Get the current time
        now = time.time()

        # Set the time Criteria
        local_time = time.localtime(now)
        time_format = '%H:%M:%S'
        time_stamp = time.strftime(time_format, local_time)

        # Update the time on the home screen
        self.clock_label.text = time_stamp

    def update_date(self, dt):
        # Get the current time/date
        today = datetime.date.today()

        # Set the date Criteria
        date_format = '%m-%d-%y'
        date_stamp = today.strftime(date_format)

        # Update the date on the home screen
        self.date_label.text = date_stamp

    def open_lockpop(self):
        # TODO Finalize design
        # TODO Finalize Layout

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
            btn_unit.add_widget(Button(id=drink_db['drinks'][i]['id'],
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
        # TODO might have to change how selected drink is passed through with dispense screen redesign

        global selected_drink
        selected_drink = instance.id

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

            if drink_db['drinks'][i]['id'] == selected_drink:
                drink_profile = drink_db['drinks'][i]

                self.name_label.text = drink_profile['name']

                self.garnish_label.text = drink_profile['garnish']

                self.instructions_label.text = drink_profile['instructions']

                img_path = '../DrinkDB_Images/{}'.format(drink_profile['img'])
                self.drink_img.source = img_path

                for j in range(len(drink_profile['ingredients'])):

                    if j == 0:
                        self.ingredient_layout.clear_widgets()

                    self.ingredient_layout.add_widget(Label(text=drink_profile['ingredients'][j],
                                                            font_size=20,
                                                            size_hint_y=None,
                                                            height=30))

                    self.ingredient_layout.add_widget(Label(text=str(drink_profile['measures'][j]) + ' OZ',
                                                            font_size=20,
                                                            size_hint_y=None,
                                                            height=30))


class CategoriesScreen(Screen):
    # TODO Fill out description, usage, and structure
    # TODO Search by letter?
    # TODO Create new design layout (user friendly, and modern)
    # TODO Define button press
    # TODO Add images to and from Base_Images

    """
    -- Description --


    -- Usage --


    -- Structure --

    """

    pass


class FilteredDrinksScreen(Screen):
    # TODO Is this needed? Try implementing filter options into all drinks screen
    # TODO Fill out description, usage, and structure

    """
    -- Description --


    -- Usage --


    -- Structure --

    """
    pass


class ShotsScreen(Screen):
    # TODO Redesign lower portion
    # TODO New images, no background or black background?
    # TODO Does this lead into a popup or into a shots 'all drinks screen'?
    # TODO Fill out description, usage, and structure

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

            btn_unit.add_widget(Button(id=drink_db['drinks'][i]['id'],
                                       background_normal=img_path,
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

    def btn_press(self, instance):
        global selected_drink
        selected_drink = instance.id

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

    create_drink_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateDrinkScreen, self).__init__(**kwargs)

        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.create_drink_layout.bind(minimum_height=self.create_drink_layout.setter('height'))
        self.create_grids()

    def create_grids(self):
        on_hand = pd.read_csv('../Dataframe/OnHand.csv')
        on_hand = on_hand.sort_values(by='Name', ascending=True)

        for i in on_hand.index:
            new_row = GridLayout(cols=7,
                                 size_hint_y=None,
                                 height=60)

            # Name Label
            new_row.add_widget(Label(text=on_hand.loc[i, 'Name'],
                                     font_size=30,
                                     text_size=(400, self.height),
                                     halign='left',
                                     valign='middle',
                                     multiline=False))

            # Ingredient ID
            new_row.add_widget(Label(id=on_hand.loc[i, 'ID'],
                                     text=on_hand.loc[i, 'ID'],
                                     font_size=30,
                                     text_size=(250, self.height),
                                     halign='left',
                                     valign='middle',
                                     multiline=False))

            # -1 Button
            new_row.add_widget(Button(id='btn(-1)_{}'.format(i),
                                      text='-1',
                                      font_size=20,
                                      size_hint_x=0.15,
                                      on_release=self.btn_press))

            # -.25 Button
            new_row.add_widget(Button(id='btn(-.25)_{}'.format(i),
                                      text='-.25',
                                      font_size=20,
                                      size_hint_x=0.15,
                                      on_release=self.btn_press))

            # Text Input
            new_row.add_widget(TextInput(id=''.format(i),
                                         size_hint_x=0.25,
                                         text='0',
                                         font_size=40,
                                         multiline=False))

            # +.25 Button
            new_row.add_widget(Button(id='btn(+.25)_{}'.format(i),
                                      text='+.25',
                                      font_size=20,
                                      size_hint_x=0.15,
                                      on_release=self.btn_press))

            # +1 Button
            new_row.add_widget(Button(id='btn(+1)_{}'.format(i),
                                      text='+1',
                                      font_size=20,
                                      size_hint_x=0.15,
                                      on_release=self.btn_press))

            # Add row to layout
            self.create_drink_layout.add_widget(new_row)

    def btn_press(self, instance):
        id_pressed = instance.id
        index = id_pressed.split('_')[1]

        if '(-1)' in id_pressed:
            for child in self.children:
                print(child)

        elif '(-.25)' in id_pressed:
            pass

        elif '(+.25)' in id_pressed:
            pass

        elif '(+1)' in id_pressed:
            pass

    def confirmation_popup(self):
        # TODO A lot of redesign work

        pop = Popup(size_hint=(0.5, 0.5),
                    auto_dismiss=False,
                    title='Dispense Drink',
                    title_align='center',
                    title_size=30)

        # Main Grid
        main_grid = GridLayout(rows=2)
        pop.add_widget(main_grid)

        # Row 1
        label1 = Label(text='Dispense Drink?',
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
        btn2.bind(on_release=self.dispense_drink)
        btn2.bind(on_release=pop.dismiss)
        anchor2.add_widget(btn2)
        btn_grid.add_widget(anchor2)

        # Add Grid 2 to Grid
        main_grid.add_widget(btn_grid)

        # Open the Popup
        pop.open()

    def dispense_drink(self, *args):
        # TODO Dispense Custom Drink
        # TODO Sends info to dispense screen where all ingredients and amounts are shown
        # TODO Custom dispense screen can have image saying custom drink

        pass


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
