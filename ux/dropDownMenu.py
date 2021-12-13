from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout

Builder.load_file('ui/dropDownMenu.kv')


class DropDownMenu(AnchorLayout):
    def __init__(self, **kwargs):
        self._parent = None
        super(DropDownMenu, self).__init__(**kwargs)
