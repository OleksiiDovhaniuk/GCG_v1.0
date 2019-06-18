import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

from file_work import FileWork
import process
from pynput import keyboard


Builder.load_string('''
<SetBtn@UbuntuBtn>:
    background_normal: 'res/images/set_btn_normal.png'
    background_down: 'res/images/set_btn_on_press.png'
    size_hint: (None, None)
    size: (130, 30)
<TruthTableScreen>:

    on_enter: 
        root.event()
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
                text: 'TRUTH TABLE SETTINGS'
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
                UbuntuTxtIn:
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
                UbuntuTxtIn:
                    size_hint: (1, None)
                    size: (100, 30)
                    id: tin_output_signals
                    multiline: False
                SetBtn:
                    id: btn_set_outputs
                    text: 'set outputs'
                    on_release: root.set_outputs()
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, .8)
            BoxLayout:
                id: entered_inputs
            BoxLayout:
                id: entered_outputs

            
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
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = .30
                    root.manager.current = 'ActionScreen'
            SetBtn:
                id: btn_apply
                text: "apply"
                on_press:
                    root.save_truthTable()
            SetBtn:
                id: btn_ok
                text: "ok"
                on_press:
                    root.save_truthTable()
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

    def set_inputs(self):
        pass

    def set_outputs(self):
        pass
        
    def save_truthTable(self):
        pass

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
