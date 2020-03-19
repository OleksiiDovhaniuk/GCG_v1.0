from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from control.dialog import TruthTable
from control.layout import LayoutConf
from control.lbl import Lbl
from control.textInput import RangeFilteredInput
from control.radioButton import RbtEndCondition
from control.popup import WhitePopup
from control.dialog import Load, Save

import file_work as fw
import os


Builder.load_file('view/sideConfigurations.kv')

class SideConf(BoxLayout):
    def show_save(self):
        content = Save(save=self.save, 
                    cancel=self.dismiss_popup,
                    data=self.data)
        self._popup = WhitePopup(title="Save file",
                            content=content)
        self._popup.open()

    def show_load(self):
        content = Load(load=self.load, 
                    cancel=self.dismiss_popup)
        self._popup = WhitePopup(title="Open file",
                            content=content)
        self._popup.open()

    def save(self, path, filename):        
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(str(self.data))
        self.dismiss_popup()
        

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.data = stream.read()
        self.dismiss_popup()
        
    
    def dismiss_popup(self):
        self._popup.dismiss()

class Algorithm(SideConf):
    saved_conf = fw.read_configurations()
    active_conf = saved_conf
    inputs = {}
    layouts_end_condition = {}
    color_disable = (.8, .8, .8, 1)
    hint_color_normal = (.4, .4, .4, 1)
    color_normal = (0, 0, 0, 1)
    minimise = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)
        saved_conf = self.saved_conf
        for key in saved_conf:
            layout = LayoutConf()
            label = Lbl(text=key)
            text_input = RangeFilteredInput(hint_text=f'{saved_conf[key]["value"]}',
                input_filter=saved_conf[key]['type'],
                valid_range = saved_conf[key]['range'])
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
            self.ids.algorithm_cont.add_widget(layout) 
        for key in self.layouts_end_condition:
            radio_btn = self.layouts_end_condition[key]['RadioButton']
            radio_btn.bind(on_press=self.swap_end_conditions)
        self.ids.algorithm_cont.add_widget(BoxLayout()) 

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

    def save_conf(self):
        if self.valid(): 
            self.data = self.active_conf
            self.show_save()
        else:
            self.active_conf = self.save_conf 
    
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            str_data = stream.read()
        try:
            self.saved_conf = eval(str_data)
            self.refresh_widgets()
        except SyntaxError:
            print(f'File {filename[0]} is corrupted')
            return 
        self.dismiss_popup()
        

    def save(self, path, filename):        
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(str(self.data))
        self.refresh_widgets()
        self.dismiss_popup()

    def valid(self):
        valid = True 
        active_conf = self.saved_conf
        inputs = self.inputs
        range_paar = []
        for key in inputs:
            btn = inputs[key]['RadioButton']
            txt_input = inputs[key]['TextInput']
            txt = txt_input.text
            if len(txt)>0:
                range_min = txt_input.valid_range[0]
                range_max = txt_input.valid_range[1]
                try:
                    min_value = float(range_min)
                except ValueError:
                    try:
                        min_value = float(active_conf[range_min]['value'])
                        range_paar.append([range_min, key])
                    except ValueError:
                        valid = False
                        txt_input.text = ''
                        print(f'A min value of the range of an active configuration {active_conf[key]} is corrupted') 
                try:
                    max_value = float(range_max)
                except ValueError:
                    try: 
                        max_value = float(active_conf[range_max]['value'])
                        range_paar.append([key, range_max])
                    except ValueError:
                        valid = False
                        txt_input.text = ''
                        print(f'A max value of the range of an active configuration {active_conf[key]} is corrupted') 
                try:
                    txt_float = float(txt)
                except ValueError:
                    valid = False
                    txt_input.text = ''
                    print(f'Value in "{key}" is not appropriate')
                    print(f'... or not in range [{txt_input.valid_range[0]}, {txt_input.valid_range[1]}]') 
                if  min_value <= txt_float <=  max_value:
                    try:
                        txt_int = int(txt)
                        active_conf[key]['value'] = str(txt_int)
                    except ValueError:
                        active_conf[key]['value'] = str(txt_float)
                else:
                    valid = False
                    txt_input.text = ''
                    print(f'Value in "{key}" is out of range') 
            if btn:
                active_conf[key]['active'] = btn.active
        for paar in range_paar:
            upper_key = paar[0]
            lower_key = paar[1]
            print(paar)
            if active_conf[upper_key]['value'] > active_conf[lower_key]['value']:
                valid = False
                inputs[upper_key]['TextInput'].text = ''
                inputs[lower_key]['TextInput'].text = ''

        self.active_conf = active_conf
        return valid

    def refresh_widgets(self):
        self.active_conf = self.saved_conf
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


class Inputs(SideConf):
    saved_ttbl = fw.read_truth_table()
    minimise = ObjectProperty(None)

    def show_ttbl(self, *args):
        content = TruthTable(apply=self.apply, 
                            cancel=self.dismiss_popup,
                            truth_table=self.saved_ttbl)
        self._popup = WhitePopup(title=f'{self.ids.device_name.text} Truth Table',
                            content=content)
        self._popup.open()
    

    def apply(self):        
        pass        

    def dismiss_popup(self):
        self._popup.dismiss()

class Plot(SideConf):
    minimise = ObjectProperty(None)
