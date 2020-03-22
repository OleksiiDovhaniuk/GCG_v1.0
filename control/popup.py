from kivy.lang import Builder
from kivy.uix.popup import Popup

from design import Design


Builder.load_file('view/popup.kv')

class WhitePopup(Popup):
    theme = Design().default_theme