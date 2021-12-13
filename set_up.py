from kivy.uix.screenmanager import ScreenManager
from ux.main import Main


class SetUp:
    def __init__(self):
        # The ScreenManager controls moving between screens
        self.screen_manager = ScreenManager()

    def set_up(self):
        screen_manager = self.screen_manager

        screen_manager.add_widget(Main(name = "Main"))