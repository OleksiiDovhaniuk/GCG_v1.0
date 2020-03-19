from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput


Builder.load_file('view/textInput.kv')

class RangeFilteredInput(TextInput):
    background_disabled_normal = StringProperty('atlas://res/images/defaulttheme/bg_TextInput_off')

class NameInput(TextInput):
    pass