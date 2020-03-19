from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput


Builder.load_file('view/textInput.kv')

class RangeFilteredInput(TextInput):
    background_disabled_normal = StringProperty('atlas://res/images/defaulttheme/bg_TextInput_off')
    valid_range = ObjectProperty([0, 9999])

class NameInput(TextInput):
    pass