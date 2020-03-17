import kivy
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import file_work as fw
from pandas import DataFrame
import os


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

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TTblDialog(FloatLayout):
    apply = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cells_in = None
    cells_out = None

    def __init__(self, truth_table, **kwargs):
        super(TTblDialog, self).__init__(**kwargs)
        inputs = truth_table['inputs'] 
        outputs = truth_table['outputs']
        inputs_tbl = self.ids.inputs_tbl
        outputs_tbl = self.ids.outputs_tbl
        
        row = BoxLayout(orientation='horizontal',
                        size_hint_y=None,
                        height=48) 
        row.add_widget(EmptyCell())
        key_widgets = []
        for index, key in enumerate(inputs):
            cell = TitleCell(text=key)
            row.add_widget(cell)
            key_widgets.append({key: cell})
        inputs_tbl.add_widget(row)
        self.cells_in = DataFrame(columns=key_widgets)

        for index in range(inputs.shape[0]):
            row = BoxLayout(orientation='horizontal',
                        size_hint_y=None,
                        height=48) 
            index_cell = IndexCell(index=str(index))
            row.add_widget(index_cell)
            widgets = [[]]
            for key in inputs:
                value = inputs[key][index]
                cell = Cell(text=str(value))
                row.add_widget(cell)
                widgets[0].append(cell)
            inputs_tbl.add_widget(row)
            row_df = DataFrame(data=widgets, columns=key_widgets)
            self.cells_in = self.cells_in.append(row_df)
        

class FileChooser(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text = ''

    def __init__(self, text, **kwargs):
        super(FileChooser, self).__init__(**kwargs)
        self.text = str(text)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, *args):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self, *args):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        if len(filename) > 0:
            with open(os.path.join(path, filename[0])) as stream:
                fw.save_configurations(stream.read())
        self.dismiss_popup

    def save(self, path, filename):
        if len(filename) > 0:
            txt_name = filename
            name_len = len(filename)
            if not filename[name_len-4: name_len] =='.txt':
                txt_name += '.txt'
            with open(os.path.join(path, txt_name), 'w') as stream:
                stream.write(self.text)
            self.dismiss_popup()

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

class RadioButton(CheckBox):
    pass
class RbtEndCondition(RadioButton):
    def __init__(self, **kwargs):
        super(RbtEndCondition, self).__init__(**kwargs)
        self.group = 'end_condition'
class LabelConf(Label):
    pass
class RangeFilteredInput(TextInput):
    background_disabled_normal = StringProperty('atlas://res/images/defaulttheme/bg_TextInput_off')
    valid_range = []

    def __init__(self, valid_range, **kwargs):
        super(RangeFilteredInput, self).__init__(**kwargs)
        self.valid_range = valid_range

class LayoutConf(BoxLayout):
    pass
class SideConf(BoxLayout):
    pass
class BtnSaveAs(HoverButton):
    pass
class BtnOpen(HoverButton):
    pass
class Cell(HoverButton):
    key_cell = ObjectProperty(None)
    index_cell = ObjectProperty(None)
class EmptyCell(Cell):  
    pass
class TitleCell(Cell):
    pass
class IndexCell(TitleCell):
    index = ObjectProperty(None)
class KeyCell(TitleCell):
    pass

class SideConfAlgorithm(SideConf):
    saved_conf = fw.read_configurations()
    inputs = {}
    layouts_end_condition = {}
    color_disable = (.8, .8, .8, 1)
    hint_color_normal = (.4, .4, .4, 1)
    color_normal = (0, 0, 0, 1)
    f_ch = FileChooser(saved_conf)

    def __init__(self, **kwargs):
        super(SideConfAlgorithm, self).__init__(**kwargs)
        saved_conf = self.saved_conf
        # self.f_ch.ids.btn_open.bind(on_release=self.open_with_validation)
        for key in saved_conf:
            layout = LayoutConf()
            label = LabelConf(text=key)
            text_input = RangeFilteredInput(hint_text=f'{saved_conf[key]["value"]}',
                input_filter=saved_conf[key]['type'],
                valid_range=saved_conf[key]['range'])
            layout.add_widget(label)
            radio_btn = None
            if key in ['process time', 'iterations limit']:
                radio_btn = RbtEndCondition(active=saved_conf[key]['active'])
                if not radio_btn.active:
                    label.color = self.color_disable
                    text_input.disabled = True
                layout.add_widget(radio_btn)
                self.layouts_end_condition.update({key: {'Layout': layout,
                                                    'Label': label,
                                                    'RadioButton': radio_btn,
                                                    'TextInput': text_input}})
            self.inputs.update({key: {'Layout': layout,
                                'Label': label,
                                'RadioButton': radio_btn,
                                'TextInput': text_input}})
            layout.add_widget(text_input)
            self.add_widget(layout) 
        for key in self.layouts_end_condition:
            radio_btn = self.layouts_end_condition[key]['RadioButton']
            radio_btn.bind(on_press=self.swap_end_conditions)
        layout_btns = BoxLayout(size_hint=(.95, None), 
            height=50,
            padding=(20, 5))
        btn_save = BtnSaveAs(on_release=self.save_with_validation)
        btn_open = BtnOpen(on_release=self.show_load)
        layout_btns.add_widget(btn_save)
        layout_btns.add_widget(btn_open)
        self.add_widget(BoxLayout()) 
        self.add_widget(layout_btns) 

    def swap_end_conditions(self, obj):
        layouts = self.layouts_end_condition
        if  obj.active:
            for key in layouts:
                label = layouts[key]['Label']
                text_input = layouts[key]['TextInput']
                is_r_btn_active = layouts[key]['RadioButton'].active
                if is_r_btn_active:
                    label.color = self.color_normal
                    text_input.hint_text_color = self.hint_color_normal
                else:
                    label.color = self.color_disable
                    text_input.hint_text_color = self.color_disable
                text_input.disabled = not is_r_btn_active
        obj.active = True

    def save_with_validation(self, *args):
        invalid = False 
        active_conf = self.saved_conf
        inputs = self.inputs
        for key in inputs:
            btn = inputs[key]['RadioButton']
            txt_input = inputs[key]['TextInput']
            txt = txt_input.text
            if len(txt)>0:
                try:
                    txt_float = float(txt)
                except ValueError:
                    invalid = True
                    txt_input.text = ''
                    print(f'Value in "{key}" is not appropriate') 
                if (txt_float >= txt_input.valid_range[0] and 
                    txt_float <= txt_input.valid_range[1]):
                    active_conf[key]['value'] = txt
                else:
                    invalid = True
                    txt_input.text = ''
                    print(f'Value in "{key}" is out of range') 
            if btn:
                active_conf[key]['active'] = btn.active
        if invalid: return
        self.saved_conf = active_conf
        fw.save_configurations(active_conf)
        self.f_ch.text = str(active_conf)
        self.f_ch.show_save()
        self.refresh()

    def refresh(self):
        saved_conf = self.saved_conf
        inputs = self.inputs
        for key in inputs:
            lbl = inputs[key]['Label']
            btn = inputs[key]['RadioButton']
            txt_input = inputs[key]['TextInput']
            txt_input.text = ''
            txt_input.hint_text = f'{saved_conf[key]["value"]}'
            if btn: 
                btn.active = saved_conf[key]['active']
                txt_input.disabled = not btn.active
                if btn.active:
                    lbl.color = self.color_normal
                    txt_input.hint_text_color = self.hint_color_normal
                else:
                    lbl.color = self.color_disable
                    txt_input.hint_text_color = self.color_disable

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        if len(filename) > 0:
            with open(os.path.join(path, filename[0])) as stream:
                conf_str = stream.read()
            try:
                conf = eval(conf_str)
                self.saved_conf = conf
                self.refresh()
                self._popup.dismiss()
            except SyntaxError:
                print('An error occured trying to transform dictionary from a file')
                
    def show_load(self, *args):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

class LblTTbl(Label):
    pass
class InputsLt(SideConf):
    saved_ttbl = fw.read_truth_table()

    def show_ttbl(self, *args):
        content = TTblDialog(apply=self.apply, 
                            cancel=self.dismiss_popup, 
                            truth_table=self.saved_ttbl)
        self._popup = Popup(title=f'{self.ids.device_name.text} Truth Table',
                            title_color=(0, 0, 0, 1),
                            content=content,
                            size_hint=(.92, .92))
        self._popup.open()

    def apply(self):        
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

Factory.register('Root', cls=FileChooser)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('TTblDialog', cls=TTblDialog)
Factory.register('SideConfAlgorithm', cls=SideConfAlgorithm)
Factory.register('InputsLt', cls=InputsLt)

class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.ids.btn_algorithm.bind(on_release=self.show_conf_algorithm)
        self.ids.btn_inputs.bind(on_release=self.show_conf_ttbl)
        self.ids.btn_plot.bind(on_release=self.show_conf_plot)

    def show_conf_algorithm(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_conf = SideConfAlgorithm()
        side_cont.add_widget(side_conf)
        self.ids.btn_algorithm.disabled = True
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
    
    def show_conf_ttbl(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_conf = InputsLt()
        side_cont.add_widget(side_conf)
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = True
        self.ids.btn_plot.disabled = False
    
    def show_conf_plot(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = True
