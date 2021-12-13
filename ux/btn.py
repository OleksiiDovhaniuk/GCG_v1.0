from kivy.lang import Builder
from ux.hoverBehaviour import HoverButton
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex as from_hex

from design import Design


Builder.load_file('ui/btn.kv')


class Btn(HoverButton):
    theme = Design().default_theme

    def set_color(self, color):
        if isinstance(color, str):
            self.color = from_hex(color)
        else:
            self.color = color


class SaveAsBtn(Btn):
    pass


class OpenBtn(Btn):
    pass


class IconViewBtn(Btn):
    pass


class ListViewBtn(Btn):
    pass


class EditBtn(Btn):
    pass


class ArrowBtn(Btn):
    pass


class ToolBtn(BoxLayout, Btn):
    pass


class DropDownBtn(Btn):
    def __init__(self, buttons, **kwargs):
        Btn.__init__(self, **kwargs)

        self.dropdown = dropdown = DropDown()

        for btn in buttons:
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        self.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class PropertyDropDown(DropDownBtn):

    def __init__(self, buttons, **kwargs):
        DropDownBtn.__init__(self, buttons=buttons, text=buttons[0].text)
