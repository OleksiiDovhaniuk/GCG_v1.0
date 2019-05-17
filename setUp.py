import os
from kivy.uix.screenmanager import ScreenManager
from home import HomeScreen
from truthTable import TruthTableScreen
from configurations import ConfigurationsScreen
from run import RunScreen


class SetUp:

    def __init__(self):
        # The ScreenManager controls moving between screens
        self.screen_manager = ScreenManager()

    def set_up(self):
        screen_manager = self.screen_manager

        screen_manager.add_widget(HomeScreen(name = "HomeScreen"))
        screen_manager.add_widget(TruthTableScreen(name = "TruthTableScreen"))
        screen_manager.add_widget(ConfigurationsScreen(name = "ConfigurationsScreen"))
        screen_manager.add_widget(RunScreen(name = "RunScreen"))
       