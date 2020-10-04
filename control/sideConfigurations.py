import os
from copy import deepcopy
from functools import partial

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from pandas import DataFrame

import file_work as fw
from control.cell import AddCell, Cell, EmptyCell, IndexCell, SwitchCellBtn, TitleCell
from control.dialog import Load, Save, TruthTable
from control.layout import GreyDefault, LayoutConf, TTblRow, Separator10, Line1Dark
from control.lbl import InfoCoefLbl, InfoLbl, Lbl, ResultsLbl, TitleLbl
from control.popup import WhitePopup
from control.radioButton import RbtEndCondition
from control.textInput import AlgorithmCoefInput, AlgorithmConfigsInput, DeviceNameInput
from control.widgets import HistoryWidget
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

        # Create info label.
        self.info_lbl = InfoLbl(self.ids.container)

        # Add and fill with configs scroll view.
        scroll_view = ScrollView(
            do_scroll_x=True, 
            effect_cls='ScrollEffect',
            pos_hint={'center_x': .5, 'center_y': .5},
        )
        self.cont = BoxLayout(
            orientation='vertical', 
            size_hint_y=None,
            height = 40
            )
        self.cont.padding = (40, 20)
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
                    widgets[name]['Coeficient Info'].text = f'{in_persent}%'
                    widgets[name]['Coeficient Info'].change_status_to('Help')

            elif key in ('Process Time', 'Iterations Limit'):
                self.draw_config(key, *data, radio_btn=True)
            
            else:
                self.draw_config(key, *data)
                
            self.cont.add_widget(Line1Dark())

        for key in coefs:
            mates_txtin = [widgets[k]['Text Input'] for k in coefs if k != key]
            widgets[key]['Text Input'].mates = mates_txtin

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
            
        # self.ids.container.add_widget(self.info_lbl)

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


        if not t:
            if is_coef:
                coef_lbl = InfoCoefLbl()
                widgets[name]['Coeficient Info'] = coef_lbl
                lt.add_widget(coef_lbl)
                txt_in = AlgorithmCoefInput(
                    key=name,
                    hint_text=str(value),
                    input_filter=dtype,
                    valid_range=(dmin, dmax),
                    info_label=self.info_lbl,
                    info_coef = coef_lbl,
                )
            else:
                txt_in = AlgorithmConfigsInput(
                    key=name,
                    hint_text=str(value),
                    input_filter=dtype,
                    valid_range=(dmin, dmax),
                    info_label=self.info_lbl,
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

    def save(self, file_name=None, *args):
        for key in self.data['Algorithm']['configurations']:
            if key == 'Control Gates` Number':
                for index, extreme in enumerate(('min', 'max')):
                    self.data['Algorithm']['configurations'][key]['value'][index]\
                        = self.widgets[extreme]['Text Input'].get_value()

            elif key == 'Fitness Function Coeficients':
                for index, coef in enumerate(self.COEFS):
                    self.data['Algorithm']['configurations'][key]['value'][index]\
                        = self.widgets[coef]['Text Input'].get_value()
            else:
                try:
                    self.data['Algorithm']['configurations'][key]['value']\
                        = self.widgets[key]['Text Input'].get_value()
                    self.data['Algorithm']['configurations'][key]['is active']\
                        = self.widgets[key]['Radio Button'].active
                except KeyError:
                    continue

        if file_name:
            SideConf.save(self, file_name, *args)
        else:
            fw.save()
            fw.autosave()

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

            widgets['alpha']['Text Input'].refresh_coef_info()

class Input(SideConf):
    TITLE = 'Input Editor'
    HEADER_HEIGHT = 32
    PADDING_X = 20

    def __init__(self):
        super().__init__()
        self.device = device = self.data['Device']
        cont = GreyDefault(
            orientation='vertical',
            pos_hint={'center_x': .5, 'center_y': .5},
        ) 
        self.ids.container.clear_widgets()
        self.ids.container.add_widget(cont)
        self.widgets = {}

        # Header of the input side configuration view.
        self.device_name_txtin = DeviceNameInput(
            hint_text=device['Name'],
        )
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

        cont.add_widget(Separator10())
        cont.add_widget(lt)
        cont.add_widget(GreyDefault())

        # Table history.
        ttbl_cont = BoxLayout(padding=(40, 20))
        ttbl_cont.add_widget(self.history())
        ttbl_cont.add_widget(BoxLayout(size_hint_x=None, width=20))


        self.cell_width = self.cell_height = 32
        table_size = (
            (len(self.get_titles())+3) * self.cell_width, 
            (len(self.get_values())+3) * self.cell_height,
            ) 
        # Truth table editor.
        self.ttbl = ttbl = BoxLayout(
            size_hint=(None, None),
            size=table_size,
            orientation='vertical',
            )
        scroll_view = ScrollView(
            do_scroll_x=True, 
            do_scroll_y=True, 
            effect_cls='ScrollEffect',
            size_hint=(1, 2.2),
            pos_hint={'center_x': .5, 'center_y': 1.1},
        )
        scroll_view.add_widget(ttbl)
        self.draw_truth_table()
        self.connect_truth_table()
        ttbl_cont.add_widget(scroll_view)
        cont.add_widget(ttbl_cont)

    def history(self):
        history =  BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=250,
        )

        for title in ('Inputs', 'Outputs', 'Add', 'Switch'):
            lt = BoxLayout(
                size_hint_y=None,
                height=40,
            )

            if title == 'Switch':
                description = 'Switch cell`s type'
                lt.add_widget(BoxLayout(size_hint_x=None, width=4))
            elif title == 'Add':
                description = f'{title} cells'
            else:
                description = f'{title} cell-titles'

            if title == 'Switch':
                vert_lt = BoxLayout(
                    orientation='vertical',
                    size_hint_x=None,
                    width = 24
                )
                vert_lt.add_widget(BoxLayout())
                vert_lt.add_widget(HistoryWidget(title=title))
                vert_lt.add_widget(BoxLayout())
                lt.add_widget(vert_lt)
            else:
                lt.add_widget(HistoryWidget(title=title))
            lt.add_widget(BoxLayout())
            lt.add_widget(Lbl(
                text=description,
                size_hint=(None, None),
                size=(200, 40)
            ))
            history.add_widget(lt)

        history.add_widget(BoxLayout(size_hint_y=None, height=200))
        return history

    def draw_truth_table(self):
        """ Draws thuth table mutable table in container.

        :param container: kivy widget object to graw truth table in.

        """
        data = self.device['Truth Table']
        size = len(data['inputs']) + len(data['outputs'])
        
        # Draw switch buttons.
        switches = []
        lt = BoxLayout(size_hint_y=None, height=16, spacing=8)
        lt.add_widget(BoxLayout(size_hint_x=None, width=28))

        for _ in range(size):
            switch = SwitchCellBtn()
            switches.append(switch)
            lt.add_widget(switch)

        self.widgets['Switches` Layout'] = lt
        self.widgets['Switches'] = switches
        self.ttbl.add_widget(lt)

        # Draw title cells and add cell at the end.
        titles = []
        lt = BoxLayout(size_hint_y=None, height=32)
        lt.add_widget(BoxLayout(size_hint_x=None, width=32))

        for index, signal in enumerate(data['inputs']):
            lt.width += 32
            title_cell = TitleCell(
                text=signal,
                cell_type='Input',
                index=index, 
                del_column=lambda ind: self.del_column(ind),
                get_titles=self.get_titles,
                rename_title=self.rename_title,
                save_switch=lambda title, sign_type: self.save_switch(title, sign_type),
                )
            titles.append(title_cell)
            lt.add_widget(title_cell)

        for index, signal in enumerate(data['outputs']):
            title_cell = TitleCell(
                text=signal,
                cell_type='Output',
                index=index+len(data['inputs']), 
                del_column=lambda ind: self.del_column(ind),
                get_titles=self.get_titles,
                rename_title=self.rename_title,
                save_switch=lambda title, sign_type: self.save_switch(title, sign_type),
                )
            titles.append(title_cell)
            lt.add_widget(title_cell)
    
        add_cell = AddCell()
        add_cell.bind(on_release=self.add_column)
        lt.add_widget(add_cell)
        self.widgets['Titles` Layout'] = lt
        self.widgets['Titles'] = titles
        self.widgets['Add Column Cell'] = add_cell
        self.ttbl.add_widget(lt)

        # Draw index cells and cells with values.
        values = self.get_values()
        cells = []
        layouts = []
        index_cells = []

        for index, row in enumerate(values):
            lt = BoxLayout(size_hint_y=None, height=32)
            layouts.append(lt)
            ind_cell = IndexCell(
                title=str(index+1), 
                del_row=lambda index: self.del_row(index)
                )
            index_cells.append(ind_cell)
            lt.add_widget(ind_cell)
            
            cell_row = []
            for value in row:
                cell = Cell(
                    text=str(value[1]),
                    save_value=lambda t, ind, v: self.save_value(t, ind, v),
                    bent_index=index,
                    bent_title=value[0],
                    )
                cell_row.append(cell)
                lt.add_widget(cell)
            cells.append(cell_row)
            self.ttbl.add_widget(lt)

        lt = StackLayout()
        add_cell = AddCell()
        add_cell.bind(on_release=self.add_row)
        lt.add_widget(add_cell)
        # lt.add_widget(BoxLayout())
        self.ttbl.add_widget(lt)
        self.widgets['The Last Layout'] = lt
        self.widgets['Add Row Cells'] = add_cell
        self.widgets['Cells` Layouts'] = layouts
        self.widgets['Cells'] = cells
        self.widgets['Index Cells'] = index_cells
        
    def connect_truth_table(self):
        for switch, title_cell in zip(self.widgets['Switches'], self.widgets['Titles']):
            switch.bent_title_cell = title_cell

    def get_titles(self):
        """
        Returns current set of signals titles in list.

        """
        return self.device['Truth Table']['inputs'].keys()\
            + self.device['Truth Table']['outputs'].keys()

   
    def rename_title(self, name, new_name):
        """
        Rename one of the existing signal titles.

        :param: name [str]
        :param: new_name [str]

        :side effect: the method changes self.device['Truth Table'] part of the nesty dict. 

        """
        truth_table = self.device['Truth Table']
        if name in truth_table['inputs']:
            truth_table['inputs'][new_name] = truth_table['inputs'].pop(name)
        else:
            truth_table['outputs'][new_name] = truth_table['outputs'].pop(name) 



    def get_values(self):
        """ Returns list of rows of truth table values, without signal titles.
        The data is taken from self.device.

        :return: 2d list of 0s and 1s.

        """
        ttbl = self.device['Truth Table']
        inputs = [[[key, int(signal)] for signal in ttbl['inputs'][key]] for key in ttbl['inputs']]
        outputs = [[[key, int(signal)] for signal in ttbl['outputs'][key]] for key in ttbl['outputs']]
        values = inputs
        values.extend(outputs)
        print(list(zip(*values)))

        return list(zip(*values))

    def del_row(self, index):
        self.ttbl.height -= self.cell_height
        layouts = self.widgets['Cells` Layouts']
        indices = self.widgets['Index Cells']
        cells = self.widgets['Cells']
        ttbl = self.device['Truth Table']

        self.ttbl.remove_widget(layouts[index])
        layouts.pop(index)
        cells.pop(index)
        indices.pop(index)

        for cell_row in cells[:index]:
            for cell in cell_row:
                cell.bent_index -= 1

        for sign_type in ('inputs', 'outputs'):
            for key in ttbl[sign_type]:
                ttbl[sign_type][key] = ttbl[sign_type][key][:index] + ttbl[sign_type][key][index+1:]

        for ind in range(index, len(indices)):
            indices[ind].title = str(ind+1)

        print(ttbl)
        

    def del_column(self, index):
        widgets = self.widgets
        self.ttbl.width -= self.cell_width

        widgets['Switches` Layout'].remove_widget(widgets['Switches'].pop(index))
        if widgets['Titles'][index].reserved_title in self.device['Truth Table']['inputs'].keys():
            self.device['Truth Table']['inputs'].pop(widgets['Titles'][index].reserved_title)
        elif widgets['Titles'][index].reserved_title in self.device['Truth Table']['outputs'].keys():
            self.device['Truth Table']['outputs'].pop(widgets['Titles'][index].reserved_title)

        widgets['Titles` Layout'].remove_widget(widgets['Titles'].pop(index))
        for lt, cell_row in zip(widgets['Cells` Layouts'], widgets['Cells']):
            lt.remove_widget(cell_row.pop(index))
        
        for ind in range(index, len(widgets['Titles'])):
            widgets['Titles'][ind].index -= 1

        print(self.get_titles())

    def get_titles(self):
        data = self.device['Truth Table']
        titles = list(data['inputs'].keys())
        titles.extend(list(data['outputs'].keys()))
        
        return titles

    def add_column(self, *args):
        widgets = self.widgets
        self.ttbl.width += self.cell_width

        switch = SwitchCellBtn()
        widgets['Switches'].append(switch)
        widgets['Switches` Layout'].add_widget(switch)

        index = len(widgets['Titles'])
        title_cell = TitleCell(
                        index=index, 
                        del_column=lambda ind: self.del_column(ind),
                        get_titles=self.get_titles,
                        rename_title=self.rename_title,
                        save_switch=lambda title, sign_type: self.save_switch(title, sign_type),
                        )
        print(self.device['Truth Table']['inputs'])
        column_values = ''
        for _ in range(len(widgets['Cells'])):
            column_values += '0'
        self.device['Truth Table']['inputs']['def.'] = column_values

        titles_layout = widgets['Titles` Layout']
        titles_layout.remove_widget(widgets['Add Column Cell'])
        titles_layout.add_widget(title_cell)
        widgets['Titles'].append(title_cell)
        switch.bent_title_cell = title_cell

        add_cell = AddCell()
        add_cell.bind(on_release=self.add_column)
        titles_layout.add_widget(add_cell)
        widgets['Add Column Cell'] = add_cell

        index = 0
        for lt, cell_row in zip(widgets['Cells` Layouts'], widgets['Cells']):
            cell = Cell(
                text='0',
                save_value=lambda t, ind, v: self.save_value(t, ind, v),
                bent_index=index,
                bent_title_cell=title_cell,
                )
            cell_row.append(cell)
            lt.add_widget(cell)
            index += 1 

        title_cell.focus = True

    def add_row(self, *args):
        widgets = self.widgets
        self.ttbl.height += self.cell_height
        self.ttbl.remove_widget(widgets['The Last Layout'])
        ttbl = self.device['Truth Table']
        index = len(widgets['Cells` Layouts'])

        for sign_type in ttbl:
            for key in ttbl[sign_type]:
                ttbl[sign_type][key] += '0'

        lt = BoxLayout(size_hint_y=None, height=32)
        ind_cell = IndexCell(
            title=str(index + 1), 
            del_row=lambda ind: self.del_row(ind)
            )
        widgets['Index Cells'].append(ind_cell)
        lt.add_widget(ind_cell)
        
        cell_row = []
        for title_cell in widgets['Titles']:
            cell = Cell(
                text='0',
                save_value=lambda t, ind, v: self.save_value(t, ind, v),
                bent_index=index,
                bent_title_cell=title_cell,
                )
            cell_row.append(cell)
            lt.add_widget(cell)
        widgets['Cells'].append(cell_row)
        widgets['Cells` Layouts'].append(lt)
        self.ttbl.add_widget(lt)
        self.ttbl.add_widget(widgets['The Last Layout'])

        print(ttbl)

    def save_switch(self, title, signal_type, *args):
        ttbl = self.device['Truth Table']

        if signal_type == 'Input':
           ttbl['inputs'][title] = ttbl['outputs'].pop(title)
        elif signal_type == 'Output':
           ttbl['outputs'][title] = ttbl['inputs'].pop(title)
        else:
            print('[BW] Error: switch button incorrect type.')

        print(ttbl)

    def save_value(self, title, index, value, *args):
        inputs = self.device['Truth Table']['inputs']
        outputs = self.device['Truth Table']['outputs']
        
        if title in inputs:
            inputs[title] = inputs[title][:index] + value + inputs[title][index+1:]
        elif title in outputs:
            outputs[title] = outputs[title][:index] + value + outputs[title][index+1:]
        else:
            print('ERROR: undefined cell "{}" change'.format(title))

        print(self.device['Truth Table'])

    def save(self, file_name=None, *args):
        device_name = self.device_name_txtin.text
        name = self.device['Name']
        if device_name != '':
            name = device_name
        else:
            name = self.device_name_txtin.hint_text


        if file_name:
            SideConf.save(self, name, *args)
        else:
            fw.save()
            fw.autosave()

    def load(self, file_name, *args):
        SideConf.load(self, file_name, *args)
        self.refresh_inputs()

    def refresh_inputs(self):
        self.device = self.data['Device']
        self.device_name_txtin.text = ''
        self.device_name_txtin.hint_text = self.device['Name']
        print(self.device['Name'])
        self.ttbl.clear_widgets()
        self.draw_truth_table()
        self.connect_truth_table()

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
