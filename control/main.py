import kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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

class CustomDropDown(DropDown):
    pass

class HoverButton(Button, HoverBehavior):
    pass

class DropDownBtn(HoverButton):
    def __init__(self, **kwargs):
        super(DropDownBtn, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 28)
        if self.hovered: self.background_normal = "res/images/bg_hover_button.png"
        else: self.background_normal = "res/images/bg_normal.png"
        self.font_name = 'res/fonts/source_code_pro/SourceCodePro-Medium.otf'
        self.font_size = '18sp'
        self.color = (0, 0, 0, 1)
        self.halign = 'left'
        self.valign = 'middle'
        self.pos_hint = {'center_x': .5, 'center_y': 0.5}
        self.text_size = self.size


file_dropdown = DropDown()
file_BoxLayout = BoxLayout(orientation='vertical', id='file_box', size=(100,150))
file_options = ['New', 'Open', 'Save', 'Exit']
for option in file_options:
    btn = DropDownBtn(text='    ' + option, size_hint=(None,None), size=(200,30), color=(0,0,0,1))
    btn.bind(on_release=lambda btn: file_dropdown.select(btn.text))
    file_dropdown.add_widget(btn)

class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.ids.btn_file.bind(on_release=file_dropdown.open)

    

