from kivy.properties     import ObjectProperty
from kivy.factory        import Factory
from kivy.lang           import Builder
from kivy.uix.boxlayout  import BoxLayout

from control.dialog      import TruthTable
from control.layout      import LayoutConf
from control.lbl         import Lbl
from control.textInput   import AlgorithmConfigsInput
from control.radioButton import RbtEndCondition
from control.popup       import WhitePopup
from control.dialog      import Load, Save

from design              import Design
import file_work as fw
import os


Builder.load_file('view/sideConfigurations.kv')

class SideConf(BoxLayout):
    theme    = Design().default_theme
    minimise = ObjectProperty(None)

    def show_save(self):
        content     = Save(save  =self.save, 
                           cancel=self.dismiss_popup,
                           data  =self.data)
        self._popup = WhitePopup(title  ="Save file",
                                 content=content)
        self._popup.open()

    def show_load(self):
        content     = Load(load  =self.load, 
                           cancel=self.dismiss_popup)
        self._popup = WhitePopup(title  ="Open file",
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
    saved_configs  = fw.read_configurations()
    active_configs = fw.read_configurations()

    inputs                = {}
    layouts_end_condition = {}

    color_disable         = (.8, .8, .8, 1)
    hint_color_normal     = (.4, .4, .4, 1)
    color_normal          = (0, 0, 0, 1)

    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)
        saved_configs = self.saved_configs

        for key in saved_configs:
            layout     = LayoutConf()
            label      = Lbl(text=key)
            radio_btn  = None
            text_input = AlgorithmConfigsInput(
                key         =     key,
                hint_text   =  f'{saved_configs[key]["value"]}',
                input_filter=     saved_configs[key]['type'],
                valid_range =     saved_configs[key]['range'],
                push_value  =self.update_config)

            if key in ['process time', 'iterations limit']:
                radio_btn = RbtEndCondition(active=saved_configs[key]['active'])
                if not radio_btn.active:
                    label.color         = self.color_disable
                    text_input.disabled = True
                layout.add_widget(radio_btn)
                self.layouts_end_condition.update({key: {
                    'Layout'     : layout,
                    'Label'      : label,
                    'RadioButton': radio_btn,
                    'TextInput'  : text_input}})
            else:
                layout.add_widget(BoxLayout(
                    size_hint=(None, None),
                    size     =(40, 40)))
            layout.add_widget(label)

            self.inputs.update({key: {
                'Layout'     : layout,
                'Label'      : label,
                'RadioButton': radio_btn,
                'TextInput'  : text_input}})
            layout.add_widget(text_input)
            self.ids.algorithm_cont.add_widget(layout) 

        for key in self.layouts_end_condition:
            radio_btn = self.layouts_end_condition[key]['RadioButton']
            radio_btn.bind(on_press=self.swap_end_conditions)
        self.ids.algorithm_cont.add_widget(BoxLayout()) 

    def swap_end_conditions(self, instance):
        layouts = self.layouts_end_condition
        configs = self.active_configs

        if  instance.active:
            for key in layouts:
                label           = layouts[key]['Label']
                text_input      = layouts[key]['TextInput']
                is_r_btn_active = layouts[key]['RadioButton'].active
                if is_r_btn_active:
                    label.color                = self.color_normal
                    text_input.hint_text_color = self.hint_color_normal
                    configs[key]['active'] = True
                else:
                    label     .color           = self.color_disable
                    text_input.hint_text_color = self.color_disable
                    configs[key]['active'] = False

                text_input.disabled = not is_r_btn_active

        self.active_configs = configs
        instance.active = True

    def save_conf(self):
        self.data = self.active_configs
        self.show_save()
    
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            str_data = stream.read()
        try:
            self.active_configs = eval(str_data)
            self.refresh_widgets()
        except SyntaxError:
            print(f'File {filename[0]} is corrupted')
            return 
        self.dismiss_popup()
        
    def save(self, path, filename):  
        if len(filename.replace(' ','')) == 0:
            return       
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(str(self.data))
        self.refresh_widgets()
        self.dismiss_popup()

    def refresh_widgets(self):
        saved_conf  = self.saved_conf  = self.active_configs
        inputs      = self.inputs

        for key in inputs:
            lbl                 = inputs[key]['Label']
            btn                 = inputs[key]['RadioButton']
            txt_input           = inputs[key]['TextInput']
            txt_input.text      = ''
            txt_input.hint_text = f'{saved_conf[key]["value"]}'
            if btn: 
                btn.active         = saved_conf[key]['active']
                txt_input.disabled = not btn.active
                if btn.active:
                    lbl      .color           = self.color_normal
                    txt_input.hint_text_color = self.hint_color_normal
                else:
                    lbl      .color           = self.color_disable
                    txt_input.hint_text_color = self.color_disable

    def update_config(self, instence):
        layouts_end_condition = self.layouts_end_condition
        active_configs        = self.active_configs

        range_min   = instence.valid_range[0]
        range_max   = instence.valid_range[1]
        key         = instence.key
        txt         = instence.text
        valig       = True
        range_paar  = []

        try:
            min_value = float(range_min)
        except ValueError:
            try:
                min_value = float(active_configs[range_min]['value'])
                range_paar.append([range_min, key])
            except ValueError:
                instence.text = ''
                valig = False
                print(f'A min value of the range of an active configuration {active_configs[key]} is corrupted') 

        try:
            max_value = float(range_max)
        except ValueError:
            try: 
                max_value = float(active_configs[range_max]['value'])
                range_paar.append([key, range_max])
            except ValueError:
                instence.text = ''
                valig = False
                print(f'A max value of the range of an active configuration {active_configs[key]} is corrupted')

        try:
            txt_float = float(txt)
        except ValueError:
            instence.text = ''
            valig = False
            print(f'Value in "{key}" is not appropriate')
            print(f'... or not in range [{range_min}, {range_max}]')

        if  min_value <= txt_float <=  max_value:
            try:
                txt_int = int(txt)
                active_configs[key]['value'] = str(txt_int)
            except ValueError:
                active_configs[key]['value'] = str(txt_float)
        else:
            valig = False
            instence.text = ''
            print(f'Value in "{key}" is out of range') 

        if valig: 
            self.active_configs = active_configs
            fw.save_configurations(active_configs)
        else: 
            self.active_configs = self.saved_configs
            fw.save_configurations(self.saved_configs)

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