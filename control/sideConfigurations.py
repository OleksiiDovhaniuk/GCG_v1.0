from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from control.dialog import Load, Save, TruthTable
from control.layout import LayoutConf
from control.lbl import Lbl
from control.textInput import RangeFilteredInput
from control.radioButton import RbtEndCondition
import file_work as fw


Builder.load_file('view/sideConfigurations.kv')

class SideConf(BoxLayout):
    pass

class Algorithm(SideConf):
    saved_conf = fw.read_configurations()
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
                input_filter=saved_conf[key]['type'])
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
        content = Load(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Open file",
                            content=content,
                            title_color=(0, 0, 0, 1),
                            size_hint=(1, 1),
                            background='res/images/bg_SideConf.png')
        self._popup.open()

class Inputs(SideConf):
    saved_ttbl = fw.read_truth_table()
    minimise = ObjectProperty(None)

    def show_ttbl(self, *args):
        content = TruthTable(apply=self.apply, 
                            cancel=self.dismiss_popup,
                            reset=self.reset, 
                            truth_table=self.saved_ttbl)
        self._popup = Popup(title=f'{self.ids.device_name.text} Truth Table',
                            content=content,
                            title_color=(0, 0, 0, 1),
                            size_hint=(1, 1),
                            background='res/images/bg_SideConf.png')
        self._popup.open()
    
    def reset(self):        
        pass

    def apply(self):        
        pass        

    def dismiss_popup(self):
        self._popup.dismiss()

class Plot(SideConf):
    minimise = ObjectProperty(None)

Factory.register('Algorithm', cls=Algorithm)
Factory.register('Inputs', cls=Inputs)
Factory.register('Plot', cls=Plot)