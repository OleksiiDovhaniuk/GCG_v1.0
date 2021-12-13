from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from ux.lbl import TitleLbl, PropertyLbl, SubtitleLbl

from design import Design


Builder.load_file('ui/layout.kv')


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


class Line1Dark(LightDefault):
    pass


class Line1Blue(LightDefault):
    pass


class Separator1(DefaultLayout):
    pass


class Separator10(DefaultLayout):
    pass


class ViewLayout(BoxLayout):

    def __init__(self, name, **kwargs):
        self.name = name
        BoxLayout.__init__(
            self,
            orientation='vertical',
            padding=(15, 10),
            spacing=5,
            size_hint_y=None,
            **kwargs
        )
        self.add_widget(TitleLbl(title=name))
        self.add_widget(Line1Blue())
        self.bind(minimum_height=self.setter('height'))


class PropertyLayout(BoxLayout):
    def __init__(self,
                 label='default',
                 content=None,
                 halign='right',
                 valign='middle',
                 lbl_size_hint=(1, 1),
                 lbl_size=(180, 24),
                 size_hint_y=None,
                 ):
        BoxLayout.__init__(self)
        self.label = PropertyLbl(
            title=label,
            valign=valign,
            halign=halign,
            size_hint=lbl_size_hint,
            size=lbl_size,
            size_hint_y=size_hint_y)
        self.content = content
        self.label.height = self.content.height

        self.add_widget(self.label)
        if content:
            self.add_widget(content)
        self.bind(minimum_height=self.setter('height'))


class SubtitleLayout(BoxLayout):
    def __init__(self,
                 subtitle='default',
                 content=None):
        BoxLayout.__init__(self)
        self.subtitle = SubtitleLbl(subtitle)
        self.container = BoxLayout()
        self.container.add_widget(self.subtitle)
        if content:
            self.container.add_widget(content)
        self.add_widget(self.container)
