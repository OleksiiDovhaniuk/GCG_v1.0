from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from design import Design


Builder.load_file('view/layout.kv')

class DefaultLeyout(BoxLayout):
    theme = Design().default_theme

class HorisontalMenuBar(DefaultLeyout):
    pass

class HorizontalConf(DefaultLeyout):
    pass

class VerticalMenuBar(DefaultLeyout):
    pass

class LayoutConf(DefaultLeyout):
    pass

class TTblRow(DefaultLeyout):
    pass