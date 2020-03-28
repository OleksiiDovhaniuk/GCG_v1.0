from kivy.factory         import Factory
from kivy.lang            import Builder
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.scrollview  import ScrollView
from kivy.uix.scatter     import Scatter
from kivy.properties      import ObjectProperty,\
                                 StringProperty

from control.dialog       import TruthTable
from control.layout       import LayoutConf,\
                                 GreyDefault
from control.textInput    import AlgorithmConfigsInput
from control.radioButton  import RbtEndCondition
from control.popup        import WhitePopup
from control.dialog       import Load,\
                                 Save
from control.lbl          import Lbl,\
                                 ResultsLbl,\
                                 TitleLbl

from design               import Design
from pandas               import DataFrame
import file_work as fw
import os


Builder.load_file('view/sideConfigurations.kv')

class SideConf(GreyDefault):
    theme    = Design().default_theme
    title    = StringProperty('Default Configurations')
    minimise = ObjectProperty(None)

    COLOR_DISABLED    = (.8, .8, .8, 1)
    HINT_COLOR_NORMAL = (.4, .4, .4, 1)
    COLOR_NORMAL      = (0, 0, 0, 1)

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

class SideConfBottom(BoxLayout):
    pass

class SideInputBottom(BoxLayout):
    show_ttbl  = ObjectProperty(None)
    switch_tbl = ObjectProperty(None)

    def __init__(self, show_ttbl, switch_tbl, **kwargs):
        super(SideInputBottom, self).__init__(**kwargs)
        self.show_ttbl  = show_ttbl
        self.switch_tbl = switch_tbl

class Algorithm(SideConf):
    saved_configs  = fw.read_configurations()
    active_configs = fw.read_configurations()

    inputs                = {}
    layouts_end_condition = {}

    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)
        saved_configs = self.saved_configs
        self.ids.container.clear_widgets()
        bottom = SideConfBottom()
        self.add_widget(bottom)

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
                    label.color         = self.COLOR_DISABLED
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
            self.ids.container.add_widget(layout) 

        for key in self.layouts_end_condition:
            radio_btn = self.layouts_end_condition[key]['RadioButton']
            radio_btn.bind(on_press=self.swap_end_conditions)
        self.ids.container.add_widget(BoxLayout()) 

    def swap_end_conditions(self, instance):
        layouts = self.layouts_end_condition
        configs = self.active_configs

        if  instance.active:
            for key in layouts:
                label           = layouts[key]['Label']
                text_input      = layouts[key]['TextInput']
                is_r_btn_active = layouts[key]['RadioButton'].active
                if is_r_btn_active:
                    label.color                = self.COLOR_NORMAL
                    text_input.hint_text_color = self.HINT_COLOR_NORMAL
                    configs[key]['active'] = True
                else:
                    label     .color           = self.COLOR_DISABLED
                    text_input.hint_text_color = self.COLOR_DISABLED
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
                    lbl      .color           = self.COLOR_NORMAL
                    txt_input.hint_text_color = self.HINT_COLOR_NORMAL
                else:
                    lbl      .color           = self.COLOR_DISABLED
                    txt_input.hint_text_color = self.COLOR_DISABLED

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

class Input(SideConf):
    saved_ttbl  = fw.read_truth_table()
    active_ttbl = fw.read_truth_table()
    inputs_frame  = DataFrame.from_dict(active_ttbl['inputs'])
    outputs_frame = DataFrame.from_dict(active_ttbl['outputs']).replace([None], '  X')
    str_ttbl = {'inputs' : inputs_frame.to_string(index=False), 
                'outputs': outputs_frame.to_string(index=False)}

    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.remove_widget(self.ids.container)
        self.bottom = SideInputBottom(show_ttbl=self.show_ttbl, switch_tbl=self.switch_tbl)
        self.add_widget(self.bottom)

    def show_ttbl(self, *args):
        content = TruthTable(get_ttbl=self.get_ttbl, 
                             cancel=self.dismiss_popup,
                             truth_table=self.active_ttbl)
        self._popup = WhitePopup(title=f'{self.ids.device_name.text} Truth Table',
                                 content=content)
        self._popup.open()

    def switch_tbl(self, *args):
        btn = self.bottom.ids.switch_btn
        for key in ['inputs', 'outputs']:
            if key != btn.text:
                self.ids.tbl_lbl.text = self.str_ttbl[key]
                btn.text = key
                return
    
    def get_ttbl(self, truth_table, *args):        
        self.active_ttbl = truth_table
        inputs_frame  = DataFrame.from_dict(truth_table['inputs'])
        outputs_frame = DataFrame.from_dict(truth_table['outputs']).replace([None], '  X')
        self.str_ttbl = {'inputs' : inputs_frame .to_string(index=False), 
                         'outputs': outputs_frame.to_string(index=False)}
        self.refresh_widgets()

    def refresh_widgets(self):
        self.switch_tbl()
        self.switch_tbl()
        
class Plot(SideConf):
    pass

class Results(SideConf):
    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)

        container = self.ids.container
        container.clear_widgets()

        self.lines_number  = 8
        self.lbl_height    = ResultsLbl().font_size
        scroll_view_height = 2200
        scroll_view   = ScrollView(do_scroll_y=True)

        container.add_widget(scroll_view)

        default_content_text = 'No Information is Present'
        self.widgets = {'Truth Table'    : [TitleLbl  (title='Truth Table'),
                                            ResultsLbl(text=default_content_text)],
                        'Schemes'        : [TitleLbl  (title='Schemes'),         
                                            ResultsLbl(text=default_content_text)],
                        'Genotypes'      : [TitleLbl  (title='Genotypes'),       
                                            ResultsLbl(text=default_content_text,
                                                       font_size=10)],
                        'Configurations' : [TitleLbl  (title='Configurations'), 
                                            ResultsLbl(text=default_content_text)]}

        self.inner_container = BoxLayout(orientation='vertical',
                                    size_hint_y=None,
                                    height     =scroll_view_height)
        for key in self.widgets:
            self.inner_container.add_widget(self.widgets[key][0])
            self.inner_container.add_widget(self.widgets[key][1])
        self.inner_container.add_widget(BoxLayout())
        scroll_view.add_widget(self.inner_container)

        bottom = SideConfBottom()
        self.add_widget(bottom)

    def resize_container(self):
        pass