from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox


Builder.load_file('view/radioButton.kv')

class RadioButton(CheckBox):
    pass

class RbtEndCondition(RadioButton):
    pass