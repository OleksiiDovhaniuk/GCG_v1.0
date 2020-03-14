import kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
import file_work as fw

"""Hoverable Behaviour (changing when the mouse is on the widget by O. Poyen.
License: LGPL

__author__ = 'Olivier POYEN'
Begin:
"""

from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window

class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget 
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass

from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

"""Hoverable Behaviour (changing when the mouse is on the widget by O. Poyen.
License: LGPL
The end.
"""

kivy.require('1.10.1')
Builder.load_file('view/main.kv')

class HoverButton(Button, HoverBehavior):
    pass

class DropDownBtn(HoverButton):
    def __init__(self, **kwargs):
        super(DropDownBtn, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 28
        self.font_name = 'res/fonts/source_code_pro/SourceCodePro-Medium.otf'
        self.font_size = '18sp'
        self.color = (0, 0, 0, 1)
        self.halign = 'left'
        self.valign = 'middle'
        self.text_size = self.size

class MenuDropDown(DropDown):
    def __init__(self, options_list, **kwargs):
        super(MenuDropDown, self).__init__(**kwargs)
        self.dropdown = DropDown(auto_width=False, size_hint=(None,None), width=200, pos_hint={'center_y':.855})
        self.options = options_list
        for option in self.options:
            btn = DropDownBtn(text=option)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

    def option_list(self):
        pass

class LabelConf(Label):
    pass
class TxtConf(TextInput):
    pass
class LayoutConf(BoxLayout):
    pass
class SideConf(BoxLayout):
    pass

class SideConfAlgorithm(SideConf):
    def __init__(self, **kwargs):
        super(SideConfAlgorithm, self).__init__(**kwargs)
        configurations = fw.read_configurations()
        for key in configurations:
            name = str(key).replace(" ","_")
            layout = LayoutConf(id=f'bl_{name}',)
            label = LabelConf(id=f'lbl_{name}', 
                text=key)
            text_input = TxtConf(id=f'txt_{name}', 
                text=f'{configurations[key]["value"]}')
            layout.add_widget(label)
            layout.add_widget(text_input)
            self.add_widget(layout) 
        self.add_widget(BoxLayout())

class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

    def expend_side_menu(self, instance):
        bxl_side_menu = BoxLayout()
        self.ids.add_widget(bxl_side_menu)



