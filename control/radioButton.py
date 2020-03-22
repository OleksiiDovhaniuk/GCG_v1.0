from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox

from design import Design


Builder.load_file('view/radioButton.kv')

class RadioButton(CheckBox):
    theme = Design().default_theme

class RbtEndCondition(RadioButton):
    pass