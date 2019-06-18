import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

from file_work import save_truth_table, read_truth_table
import process
from pynput import keyboard
from home import UbuntuLbl


Builder.load_string('''
<SetBtn@UbuntuBtn>:
    background_normal: 'res/images/set_btn_normal.png'
    background_down: 'res/images/set_btn_on_press.png'
    size_hint: (None, None)
    size: (130, 30)
<TruthTableScreen>:

    on_enter: 
        root.event()
        root.show_truth_table()
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, None)
            size: (100, 90)
            spacing: 10
            
            UbuntuBtn:
                id: btn_configurations
                size_hint: (1, None)
                size: (100, 30)
                text: 'go to algorithm configurations'
                on_press:
                    root.events_cencel()
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = .30
                    root.manager.current = 'ConfigurationsScreen'

            UbuntuLbl:
                text: 'TRUTH  TABLE  SETTINGS'
                font_size: 24
                size_hint: (1, None)
                size: (100, 50)
        
        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, None)
            size: (100, 130)
            spacing: 20
            padding: 30
            BoxLayout:
                spacing: 15
                orientation: 'horizontal'
                ConfTextInput:
                    size_hint: (1, None)
                    size: (100, 30)
                    id: tin_input_signals
                    multiline: False
                SetBtn:
                    id: btn_set_inputs
                    text: 'set inputs'
                    on_release: root.set_inputs()
            BoxLayout:
                spacing: 15
                orientation: 'horizontal'
                ConfTextInput:
                    size_hint: (1, None)
                    size: (100, 30)
                    id: tin_output_signals
                    multiline: False
                SetBtn:
                    id: btn_set_outputs
                    text: 'set outputs'
                    on_release: root.set_outputs()
        UbuntuLbl:
            text: 'Truth Table:'
            font_size: 18
            size_hint: (1, None)
            size: (100, 50)
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, 1)
            size: (300, 0)
            padding: 20
            spacing: 30
            BoxLayout:
                size_hint: (1, 1)
                size: (150, 0)
                id: entered_input_signals
                orientation: 'horizontal'
            BoxLayout:
                size_hint: (1, 1)
                size: (150, 0)
                id: entered_output_signals
                orientation: 'horizontal'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, None)
            size: (100, 60)
            padding: 20
            spacing: 30
            BoxLayout:
                size_hint:(.5, None)
            SetBtn:
                id: btn_cancel
                text: "cancel"
                on_press:
                    root.events_cencel()
                    root.show_truth_table()
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = .30
                    root.manager.current = 'ActionScreen'
            SetBtn:
                id: btn_apply
                text: "apply"
                on_press:
                    root.save_truth_table()
            SetBtn:
                id: btn_ok
                text: "ok"
                on_press:
                    root.save_truth_table()
                    root.events_cencel()
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = .30
                    root.manager.current = 'ActionScreen'
        BoxLayout:
            size_hint: (1, None)
            size: (400, 30)
            spacing: 0
            padding: 10
            UbuntuLbl:
                id:lblProgress
                size:(50, 15)
                size_hint: (None, None)
                text: "0%"

            ProgressBar:
                id: pbProcess
                padding: 100
                max: 1
            
            UbuntuLbl:
                size:(100, 15)
                size_hint: (None, None)
                id:lblClock
                text: "00:00:00"
''')

class TruthTableScreen(Screen):
    
    def __init__(self, **kwargs):
        super(TruthTableScreen, self).__init__(**kwargs)
        self.row_numbers = 0
        self.input_signals = {}
        self.output_signals = {}
        self.signals_in_row = 0

    def set_inputs(self):
        str_inputs = self.ids.tin_input_signals.text
        str_inputs = str_inputs.strip()
        str_inputs = str_inputs.split(' ')

        self.row_numbers += 1
        if str_inputs[0].isidentifier():
            if str_inputs[0] in self.output_signals:
                self.ids.tin_input_signals.foreground_color = (1,.2,.2,1)
                self.ids.tin_input_signals.text = \
                    f'invalid input: list with name {str_inputs[0]} is already used!'
                return
            self.input_signals[str_inputs[0]] = []
            for element in str_inputs[1:]:
                if element.isdigit():
                    if element == '1' or element == '0':
                        self.input_signals[str_inputs[0]].append(int(element))
                    else:
                        self.ids.tin_input_signals.foreground_color = (1,.2,.2,1)
                        self.ids.tin_input_signals.text = \
                            'invalid input: list, which consists of 0 or 1 is expected!'
                        self.input_signals.pop(str_inputs[0])
                        return  
                else: 
                    self.ids.tin_input_signals.foreground_color = (1,.2,.2,1)
                    self.ids.tin_input_signals.text = \
                        'invalid input: list, which consists of 0 or 1 is expected!'
                    self.input_signals.pop(str_inputs[0])
                    return   
        else:
            self.ids.tin_input_signals.foreground_color = (1,.2,.2,1)
            self.ids.tin_input_signals.text = 'invalid input: signal`s name is expected!'
            return
        if list(self.input_signals.keys()).index(str_inputs[0]) == 0:
            self.signals_in_row = len(self.input_signals[str_inputs[0]])
            for key in self.input_signals:
                if len(self.input_signals[key]) < self.signals_in_row:
                    for _ in range(self.signals_in_row - len(self.input_signals[key])):
                        self.input_signals[key].append(0)
                elif len(self.input_signals[key]) > self.signals_in_row:
                    for index, _ in enumerate(self.input_signals[key][self.signals_in_row:]):
                       self.input_signals[key].pop(index)
            for key in self.output_signals:
                if len(self.output_signals[key]) < self.signals_in_row:
                    for _ in range(self.signals_in_row - len(self.output_signals[key])):
                        self.output_signals[key].append(None)
                elif len(self.output_signals[key]) > self.signals_in_row:
                    for index, _ in enumerate(self.output_signals[key][self.signals_in_row:]):
                       self.output_signals[key].pop(index)
        else:
            if len(self.input_signals[str_inputs[0]]) < self.signals_in_row:
                for _ in range(self.signals_in_row - len(self.input_signals[str_inputs[0]])):
                    self.input_signals[str_inputs[0]].append(0)
            elif len(self.input_signals[str_inputs[0]]) > self.signals_in_row:
                for index, _ in enumerate(self.input_signals[str_inputs[0]][ self.signals_in_row:]):
                    self.input_signals[str_inputs[0]].pop(index)

        self.ids.entered_input_signals.clear_widgets()    
        self.ids.entered_output_signals.clear_widgets()    
        for key in self.input_signals:
            str_set = ''
            str_set += key
            for value in self.input_signals[key]:
                str_set += f'\n{str(value)}'
            self.signals_row = \
                UbuntuLbl(id=f'lblSignalsRow{key}', text=str_set)
            self.ids.entered_input_signals.add_widget(self.signals_row)
        for key in self.output_signals:
            str_set = ''
            str_set += key
            for value in self.output_signals[key]:
                if value != None:
                    str_set += f'\n{str(value)}'
                else:
                    str_set += '\nX'
            self.signals_row = \
                UbuntuLbl(id=f'lblSignalsRow{key}', text=str_set)
            self.ids.entered_output_signals.add_widget(self.signals_row)

    def set_outputs(self):
        str_inputs = self.ids.tin_output_signals.text
        str_inputs = str_inputs.strip()
        str_inputs = str_inputs.split(' ')

        self.row_numbers += 1
        if str_inputs[0].isidentifier():
            if str_inputs[0] in self.input_signals:
                self.ids.tin_output_signals.foreground_color = (1,.2,.2,1)
                self.ids.tin_output_signals.text = \
                    f'invalid input: list with name {str_inputs[0]} is already used!'
                return
            self.output_signals[str_inputs[0]] = []
            for element in str_inputs[1:]:
                if element.isdigit():
                    if element == '1' or element == '0':
                        self.output_signals[str_inputs[0]].append(int(element))
                    else:
                        self.output_signals[str_inputs[0]].append(None)
                elif element == 'x' or element == 'X':
                    self.output_signals[str_inputs[0]].append(None)
                else: 
                    self.ids.tin_output_signals.foreground_color = (1,.2,.2,1)
                    self.ids.tin_output_signals.text = \
                        'invalid input: list, which consists of 0 or 1 is expected!'
                    self.output_signals.pop(str_inputs[0])
                    return   
        else:
            self.ids.tin_output_signals.foreground_color = (1,.2,.2,1)
            self.ids.tin_output_signals.text = 'invalid input: signal`s name is expected!'
            return
        if len(self.output_signals[str_inputs[0]]) < self.signals_in_row:
            for _ in range(self.signals_in_row - len(self.output_signals[str_inputs[0]])):
                self.output_signals[str_inputs[0]].append(None)
        elif len(self.output_signals[str_inputs[0]]) > self.signals_in_row:
            for index, _ in enumerate(self.output_signals[str_inputs[0]][ self.signals_in_row:]):
                self.output_signals[str_inputs[0]].pop(index)

        self.ids.entered_output_signals.clear_widgets()    
        for key in self.output_signals:
            str_set = ''
            str_set += key
            for value in self.output_signals[key]:
                if value != None:
                    str_set += f'\n{str(value)}'
                else:
                    str_set += '\nX'
            self.signals_row = \
                UbuntuLbl(id=f'lblSignalsRow{key}', text=str_set)
            self.ids.entered_output_signals.add_widget(self.signals_row)

    def save_truth_table(self):
        truth_table = {
            'inputs':   self.input_signals,
            'outputs':  self.output_signals
        }
        save_truth_table(truth_table)

    def show_truth_table(self):
        truth_table = read_truth_table()
        self.input_signals = truth_table['inputs']
        self.output_signals = truth_table['outputs']

        self.ids.entered_input_signals.clear_widgets()    
        self.ids.entered_output_signals.clear_widgets()    
        for key in self.input_signals:
            str_set = ''
            str_set += key
            for value in self.input_signals[key]:
                str_set += f'\n{str(value)}'
            self.signals_row = \
                UbuntuLbl(id=f'lblSignalsRow{key}', text=str_set)
            self.ids.entered_input_signals.add_widget(self.signals_row)
        for key in self.output_signals:
            str_set = ''
            str_set += key
            for value in self.output_signals[key]:
                if value != None:
                    str_set += f'\n{str(value)}'
                else:
                    str_set += '\nX'
            self.signals_row = \
                UbuntuLbl(id=f'lblSignalsRow{key}', text=str_set)
            self.ids.entered_output_signals.add_widget(self.signals_row)

    def show_progress(self, *args):
        if not process.is_process:
            self.ids.lblProgress.text = "0%"
            self.ids.pbProcess.value = 0
            self.ids.lblClock.text = "00:00:00"
        elif process.is_finished:
            self.ids.lblProgress.text = "100%"
            self.ids.pbProcess.value = 1
            self.ids.lblClock.text = process.time
        else:
            portion_is_ready = process.iteration / process.generations_number
            self.ids.lblProgress.text = str(round(portion_is_ready * 100)) + "%"
            self.ids.pbProcess.value = portion_is_ready
            self.ids.lblClock.text = process.time

    def on_press(key, *args):
        keys=[]
        try: k = key.char # single-char keys
        except: k = key.name # other keys
        #if key == keyboard.Key.esc: return False # stop listener
        if k in ['down', 'left', 'right',"up"]: # keys interested
            # self.keys.append(k) # store it in global-like variable
            #print('Key pressed: ' + k)
            keys.append(k)

        

    def event(self, *args):
        self.event = Clock.schedule_interval(self.show_progress, 0.025)
    
    def events_cencel(self, *args):
        self.event.cancel()
