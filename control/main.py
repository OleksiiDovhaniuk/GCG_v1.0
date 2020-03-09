import kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

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
        self.dropdown = DropDown(auto_width=False, size_hint=(None,None), width=200, pos_hint={'center_y':.855})
        self.options = options_list
        for option in self.options:
            btn = DropDownBtn(text=option)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        super(MenuDropDown, self).__init__(**kwargs)

    def option_list(self):
        pass

options_file = ['New', 'Open', 'Save', 'Exit']
options_edit = ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']
options_run = ['Run', 'Pause', 'Stop']
options_help = ['Welcome', 'Documentation', 'About']
dropdown_file = MenuDropDown(options_file)
dropdown_edit = MenuDropDown(options_edit)
dropdown_run = MenuDropDown(options_run)
dropdown_help = MenuDropDown(options_help)


class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.ids.btn_file.bind(on_release=dropdown_file.open)
        self.ids.btn_edit.bind(on_release=dropdown_edit.open)
        self.ids.btn_run.bind(on_release=dropdown_run.open)
        self.ids.btn_help.bind(on_release=dropdown_help.open)

    

