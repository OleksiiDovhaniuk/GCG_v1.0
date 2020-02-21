import os
from kivy.uix.screenmanager import ScreenManager
from control.main import Main
from truthTable import TruthTableScreen
from configurations import ConfigurationsScreen
from action import ActionScreen


class Prep:

    def __init__(self):
        # The ScreenManager controls moving between screens
        self.screen_manager = ScreenManager()

    def prep(self):
        screen_manager = self.screen_manager

        screen_manager.add_widget(Main(name = "Main"))
       