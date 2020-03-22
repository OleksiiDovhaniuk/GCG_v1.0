from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from functools import partial
from design import Design


Builder.load_file('view/textInput.kv')

class TxtInput(TextInput):
    theme = Design().default_theme

class RangeFilteredInput(TxtInput):
    valid_range = ObjectProperty([0, 9999])

class NameInput(TxtInput):
    def select_textinput(self):
        if self.focus:
            Clock.schedule_once(lambda dt: self.select_all())
