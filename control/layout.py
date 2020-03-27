from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from design import Design


Builder.load_file('view/layout.kv')

class DefaultLayout(BoxLayout):
    theme = Design().default_theme

class GreyDefault(DefaultLayout):
    pass

class LightDefault(DefaultLayout):
    pass

class DarkDefault(DefaultLayout):
    pass

class WhiteDefault(DefaultLayout):
    pass

class HorisontalMenuBar(DefaultLayout):
    pass

class HorizontalConf(DefaultLayout):
    pass

class VerticalMenuBar(DefaultLayout):
    pass

class LayoutConf(DefaultLayout):
    pass

class TTblRow(DefaultLayout):
    pass

class Separator1(DefaultLayout):
    pass

class Separator10(DefaultLayout):
    pass