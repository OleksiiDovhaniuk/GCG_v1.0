import os
from copy import deepcopy
from functools import partial

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from pandas import DataFrame

import file_work as fw
from control.cell import AddCell, Cell, EmptyCell, IndexCell, TitleCell
from control.dialog import Load, Save, TruthTable
from control.layout import GreyDefault, LayoutConf, TTblRow, Separator10
from control.lbl import InfoConfigLbl, Lbl, ResultsLbl, TitleLbl
from control.popup import WhitePopup
from control.radioButton import RbtEndCondition
from control.textInput import AlgorithmCoefInput, AlgorithmConfigsInput, TxtInput
from design import Design


Builder.load_file('view/sideConfigurations.kv')

class SideConfBottom(BoxLayout):
    pass

class SideConf(GreyDefault):
    _theme = Design().default_theme
    C_DISABLED = (.8, .8, .8, 1)
    C_NORMAL = (0, 0, 0, 1)

    def __init__(self):
        super().__init__()
        self.data = fw.read()
        bottom = SideConfBottom()
        self.ids.bottom_container.add_widget(bottom)
        bottom.ids.save_as_btn.bind(on_release=self.show_save)
        bottom.ids.open_btn.bind(on_release=self.show_load)

    def show_save(self, *args):
        content = Save(save=self.save, cancel=self.dismiss_popup)
        self._popup = WhitePopup(title="Save file", content=content)
        self._popup.open()

    def show_load(self, *args):
        content = Load(load=self.load, cancel=self.dismiss_popup)
        self._popup = WhitePopup(title="Open file", content=content)
        self._popup.open()

    def save(self, file_name):  
        fw.save(self.data, name=file_name)      
        fw.save(self.data)      
        fw.autosave(self.data)      
        self.dismiss_popup()
        
    def load(self, file_name):
        if file_name:
            self.data = fw.read(name=file_name)      
            self.dismiss_popup()
        
    def dismiss_popup(self):
        self._popup.dismiss()

class Algorithm(SideConf):
    TITLE = 'Algorithm Configurations'
    COEFS = ('alpha', 'betta', 'gamma', 'lambda')

    def __init__(self):
        super().__init__()
        self.configs = configs = self.data['Algorithm']['configurations']
        self.widgets = widgets = {}
        self.ids.container.clear_widgets()
        scroll_view = ScrollView(do_scroll_x=True, effect_cls='ScrollEffect')
        self.cont = BoxLayout(orientation='vertical', size_hint_y=None, height=10)
        self.cont.padding = (40, 0)
        coefs = self.COEFS

        scroll_view.add_widget(self.cont)
        self.ids.container.add_widget(scroll_view)        

        for key in configs:
            data = [configs[key][dkey] for dkey in configs[key]]

            if key == 'Control Gates` Number':
                self.draw_config(key, t=True)
                for name, dvalue in zip(('min', 'max'), data[0]):
                    self.draw_config(name, dvalue, *data[1:4], intent=1)

            elif key == 'Fitness Function Coeficients':
                self.draw_config(key, t=True)
                dsum = sum(data[0])
                for name, dvalue in zip(coefs, data[0]):
                    self.draw_config(name, dvalue, *data[1:4], intent=1, is_coef=True)
                    in_persent = dvalue / dsum * 100
                    in_persent = round((in_persent - (in_persent % .05)), 1)
                    widgets[name]['Info'].text = f'{in_persent}%'
                    widgets[name]['Info'].change_status_to('Help')

            elif key in ('Process Time', 'Iterations Limit'):
                self.draw_config(key, *data, radio_btn=True)
            
            else:
                self.draw_config(key, *data)

        for key in coefs:
            info_lbls = [widgets[k]['Text Input'] for k in coefs if k != key]
            widgets[key]['Text Input'].mates = info_lbls

        self.bend_related_extremes()
        widgets['Process Time']['Radio Button'].mates = [widgets['Iterations Limit']]
        widgets['Iterations Limit']['Radio Button'].mates = [widgets['Process Time']]

    def bend_related_extremes(self):
        """ Bends related text inputs based on min and max range values.

        """
        txt_inputs = [
            self.widgets[key]['Text Input'] 
            for key in self.widgets 
            if self.widgets[key].get('Text Input', None)
        ]

        for inpt in txt_inputs:
            if type(inpt.valid_range[0]) == str:
                inpt.related_min = self.widgets[inpt.valid_range[0]]['Text Input']
            
            if type(inpt.valid_range[1]) == str:
                inpt.related_max = self.widgets[inpt.valid_range[1]]['Text Input']
            
    def draw_config(self, name, value=None, dtype=None, dmin=None, dmax=None, dactive=False, dgroup=None, intent=0, t=False, radio_btn=False, is_coef=False):
        """ Method draws one configuration item from the saved in file data.json.

        Args:
            name [str];
            value [int, float];
            dtype ("int", "float");
            dmin [int, float, str];
            dmax [int, float, str];
            dactive [bool];
            dgroup [int, str];
            intent [int];
            t [bool]: configuration has list of values;
            radio_btn [bool]: configuration line has radio button;
            is_coef [bool];

        """
        widgets = self.widgets
        tab_size = 40
        lt = LayoutConf()
        lt.spacing = 10
        lt.add_widget(BoxLayout(size_hint_x=None, width=tab_size*intent))
        widgets[name] = {}
        widgets[name]['Layout'] = lt

        if radio_btn:
            rd_btn = RbtEndCondition(active=dactive, group=dgroup)
            lt.add_widget(rd_btn)
            widgets[name]['Radio Button'] = rd_btn

        lbl = Lbl(text=name)
        lt.add_widget(lbl)
        widgets[name]['Label'] = lbl

        info_lbl = InfoConfigLbl()
        lt.add_widget(info_lbl)
        widgets[name]['Info'] = info_lbl

        if not t:
            if is_coef:
                txt_in = AlgorithmCoefInput(
                    key=name,
                    hint_text=str(value),
                    input_filter=dtype,
                    valid_range=(dmin, dmax),
                    info_label=info_lbl,
                )
            else:
                txt_in = AlgorithmConfigsInput(
                    key=name,
                    hint_text=str(value),
                    input_filter=dtype,
                    valid_range=(dmin, dmax),
                    info_label=info_lbl,
                )
            lt.add_widget(txt_in)
            widgets[name]['Text Input'] = txt_in

        if radio_btn:
            rd_btn.label = lbl
            if not rd_btn.active:
                lbl.color = self.C_DISABLED
                txt_in.disabled = True

            if not t:
                rd_btn.text_input = txt_in
         
        self.cont.height += lt.height
        self.cont.add_widget(lt)

    def show_save(self, *args):
        for key in self.data['Algorithm']['configurations']:
            try:
                self.data['Algorithm']['configurations'][key]['value']\
                    = self.widgets[key]['Text Input'].get_value()
                self.data['Algorithm']['configurations'][key]['is active']\
                    = self.widgets[key]['Radio Button'].active
            except KeyError:
                continue
        
        SideConf.show_save(self)

    def save(self, file_name, *args):
        SideConf.save(self, file_name, *args)
        self.refresh_inputs()

    def load(self, file_name, *args):
        SideConf.load(self, file_name, *args)
        self.refresh_inputs()

    def refresh_inputs(self):
        configs = self.configs = self.data['Algorithm']['configurations']
        widgets = self.widgets

        for key in configs:
            if key == 'Control Gates` Number':
               for index, key2 in enumerate(('min', 'max')):
                    widgets[key2]['Text Input'].text = ''
                    widgets[key2]['Text Input'].hint_text = str(configs[key]['value'][index])

            elif key == 'Fitness Function Coeficients':
                for index, key2 in enumerate(self.COEFS):
                    widgets[key2]['Text Input'].text = ''
                    widgets[key2]['Text Input'].hint_text = str(configs[key]['value'][index])

            elif key in ('Process Time', 'Iterations Limit'):
                widgets[key]['Text Input'].text = ''
                widgets[key]['Text Input'].hint_text = str(configs[key]['value'])
                widgets[key]['Radio Button'].set_status(configs[key]['is active'])
            
            else:
                widgets[key]['Text Input'].text = ''
                widgets[key]['Text Input'].hint_text = str(configs[key]['value'])

class Input(SideConf):
    TITLE = 'Input Editor'
    HEADER_HEIGHT = 32
    PADDING_X = 20

    def __init__(self):
        super().__init__()
        self.ttbl = ttbl = self.data['Truth Table']
        contr = self.ids.container
        self.widgets = []

        # Header of the input side configuration view.
        contr.clear_widgets()
        self.device_name_txtin = TxtInput(
            hint_text='Untitled',
        )
        self.device_name_txtin.halign='center'
        lt = GreyDefault(
            orientation='horizontal', 
            size_hint_y=None,
            height=self.HEADER_HEIGHT,
            padding=(self.PADDING_X, 0),
        )
        lt.add_widget(
            Lbl(
                text='Device Name:',
                size_hint_x=None,
                width=140
            )
        )
        lt.add_widget(self.device_name_txtin)

        contr.add_widget(Separator10())
        contr.add_widget(lt)
        contr.add_widget(GreyDefault())



            
class Plot(SideConf):
    TITLE = 'Plot View/Configurations'

class Results(SideConf):
    TITLE = 'Results'

    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)
        self.remove_widget(self.ids.container)

        self.add_widget(SideConfBottom())

    def resize_container(self):
        self.ids.side_results_container.height=5000
