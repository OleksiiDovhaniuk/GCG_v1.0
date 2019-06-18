import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from functools import partial

from home import UbuntuLbl
from file_work import save_configurations, read_configurations
import process

Builder.load_string('''
<ConfTextInput@TextInput>:
    size_hint: (1, None)
    size: (100, 30)
    foreground_color: (.3, .3, .3, 1)
    on_touch_down: 
        if self.collide_point(*args[1].pos): self.foreground_color = (0, 0, 0, 1)
        if self.collide_point(*args[1].pos): self.text = ""
<ConfLbl@UbuntuLbl>:
    size_hint: (None, None)
    size: (160, 30)
    text_size: self.size
    halign: 'left'
    valign: 'middle'
<ConfigurationsScreen>:
    on_enter: 
        root.show_configurations()
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
                text: 'go to truth table settings'
                on_press:
                    root.events_cencel()
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = .30
                    root.manager.current = 'TruthTableScreen'

            UbuntuLbl:
                text: 'ALGORITHM CONFIGURATIONS'
                font_size: 24
                size_hint: (1, None)
                size: (100, 50)
        
        BoxLayout:
            orientation: 'vertical'
            size_hint:(1, None)
            size: (100, 420)
            padding: 30
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, None)
                size: (100, 252)
                BoxLayout:
                    ConfLbl:
                        id: lblGenerationSize
                        text: "Generation Size"
                    ConfTextInput:
                        id: tinGenerationSize
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        id: lblChromosomeSize
                        text: "Chromosome Size"
                    ConfTextInput:
                        id: tinChromosomeSize
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        id: lblCrossover
                        text: "Crossover Chance"
                    ConfTextInput:
                        id: tinCrossover
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        id: lblMutation
                        text: "Mutation Chance"
                    ConfTextInput:
                        id: tinMutation
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        text: 'Finish Priority'
                    ClearBtn:
                        id: btn_time
                        size_hint:(None, None)
                        size: (145, 30)
                        orientation: 'horizontal'
                    ClearBtn:
                        id: btn_iterations
                        size_hint:(None, None)
                        size: (145, 30)
                        orientation: 'horizontal'
                BoxLayout:
                    id: boxFinishValue
                    ConfLbl:
                        id: lblFinishValue
                        text: 'Max Iterations'
                    ConfTextInput:
                        id: tinFinishValue
                        multiline: False

            BoxLayout:
                orientation: 'vertical'
                size_hint:(1, None)
                size: (100, 126)
                BoxLayout:
                    ConfLbl:
                        id: lblGarbageOutputs
                        text: "Garbage Outputs"
                    ConfTextInput:
                        id: tinGarbageOutputs
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        id: lblDelay
                        text: "Delay (ns)"
                    ConfTextInput:
                        id: tinDelay
                        multiline: False
                BoxLayout:
                    ConfLbl:
                        id: lblQuantumCost
                        text: "Quantum Cost"
                    ConfTextInput:
                        id: tinQuantumCost
                        multiline: False
        BoxLayout:
            # Make some empty space 
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, None)
            size: (100, 40)
            padding: 20
            spacing: 30
            BoxLayout:
                size_hint:(.5, None)
            SetBtn:
                id: btn_cancel
                text: "cancel"
                on_press:
                    root.events_cencel()
                    root.show_configurations()
                    root.manager.transition.direction = 'right'
                    root.manager.transition.duration = .30
                    root.manager.current = 'ActionScreen'
            SetBtn:
                id: btn_apply
                text: "apply"
                on_press:
                    root.save_configurations()
            SetBtn:
                id: btn_ok
                text: "ok"
                on_press:
                    root.save_configurations()
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
class ConfLbl(UbuntuLbl):
    pass

class ConfTextInput(TextInput):
    pass

class ConfigurationsScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigurationsScreen, self).__init__(**kwargs)
        # self.ids.tinGenerationSize.text = self.fileWork.str_generationSize()
        # self.ids.tinChromosomeSize.text = self.fileWork.str_genesNumber()
        # self.ids.tinCrossover.text = self.fileWork.str_crossingChance()
        # self.ids.tinMutation.text = self.fileWork.str_mutationChance()

        self.chx_box_iterations = CheckBox(active=True, size_hint=(None, 1), size=(30, 10))
        self.chx_box_time = CheckBox(active=False, size_hint=(None, 1), size=(30, 10))
        self.chx_box_iterations.bind(on_press=partial(self.switch_check_box, self.chx_box_iterations))
        self.chx_box_time.bind(on_press=partial(self.switch_check_box, self.chx_box_time))
        self.ids.btn_iterations.add_widget(self.chx_box_iterations)
        self.ids.btn_iterations.add_widget(ConfLbl(text='by iterations', size_hint=(None, 1), size=(100, 10)))
        self.ids.btn_time.add_widget(self.chx_box_time)
        self.ids.btn_time.add_widget(ConfLbl(text='by time', size_hint=(None, 1), size=(100, 10)))

    def show_configurations(self):
        configurations = read_configurations()
        foreground_color = (.3, .3, .3, 1)
        self.ids.tinGenerationSize.foreground_color = foreground_color
        self.ids.tinChromosomeSize.foreground_color = foreground_color
        self.ids.tinCrossover.foreground_color = foreground_color
        self.ids.tinMutation.foreground_color = foreground_color
        self.ids.tinFinishValue.foreground_color = foreground_color
        self.ids.tinGarbageOutputs.foreground_color = foreground_color
        self.ids.tinDelay.foreground_color = foreground_color
        self.ids.tinQuantumCost.foreground_color = foreground_color
        
        self.ids.tinGenerationSize.text = str(configurations['generation size'])
        self.ids.tinChromosomeSize.text = str(configurations['chromosome size'])
        self.ids.tinCrossover.text = str(configurations['crossover chance'])
        self.ids.tinMutation.text = str(configurations['mutation chance'])
        if 'iterations limit' in configurations:
            self.switch_check_box(self.chx_box_iterations)
            self.ids.tinFinishValue.text = str(configurations['iterations limit'])
            self.ids.lblFinishValue.text = 'Max Iterations'
        else:
            self.switch_check_box(self.chx_box_time)
            self.ids.tinFinishValue.text = str(configurations['time limit'])
            self.ids.lblFinishValue.text = 'Time Limit (min)'
        self.ids.tinGarbageOutputs.text = str(configurations['garbage outputs'])
        self.ids.tinDelay.text = str(configurations['delay'])
        self.ids.tinQuantumCost.text = str(configurations['quantum cost'])

    
    def save_configurations(self):
        if self.valid_configations():
            if self.chx_box_iterations.active:
                limits_type = 'iterations limit'
            else:
                limits_type = 'time limit'

            configurations = {
                'generation size':  self.ids.tinGenerationSize.text,
                'chromosome size':  self.ids.tinChromosomeSize.text,
                'crossover chance': self.ids.tinCrossover.text,
                'mutation chance':  self.ids.tinMutation.text,
                f'{limits_type}':   self.ids.tinFinishValue.text,
                'garbage outputs':  self.ids.tinGarbageOutputs.text,
                'delay':            self.ids.tinDelay.text,
                'quantum cost':     self.ids.tinQuantumCost.text
                }
            save_configurations(configurations)

    def valid_configations(self):
        are_valid = []
        are_valid.append(self.try_read_int_text_input(self.ids.tinGenerationSize))
        are_valid.append(self.try_read_int_text_input(self.ids.tinChromosomeSize))
        are_valid.append(self.try_read_float_text_input(self.ids.tinCrossover))
        are_valid.append(self.try_read_float_text_input(self.ids.tinMutation))
        are_valid.append(self.try_read_int_text_input(self.ids.tinFinishValue))
        are_valid.append(self.try_read_int_text_input(self.ids.tinGarbageOutputs))
        are_valid.append(self.try_read_int_text_input(self.ids.tinDelay))
        are_valid.append(self.try_read_int_text_input(self.ids.tinQuantumCost))
        return not False in are_valid

    def try_read_int_text_input(self, text_input):
        try:
            digit_input = int(text_input.text)
            if digit_input > 0:
                return True
            else:
                text_input.foreground_color = (1,.2,.2,1)
                text_input.text = 'invalid input: expected int digit > 0!'
                return False
        except ValueError:
            text_input.foreground_color = (1,.2,.2,1)
            text_input.text = 'invalid input: expected int type digit!'
            return False
    def try_read_float_text_input(self, text_input):
        try:
            digit_input = float(text_input.text)
            if digit_input >= 0 and digit_input <= 1:
                return True
            else:
                text_input.foreground_color = (1,.2,.2,1)
                text_input.text = 'invalid input: expected float digit in [0,1]!'
                return False
        except ValueError:
            text_input.foreground_color = (1,.2,.2,1)
            text_input.text = 'invalid input: expected float type digit!'
            return False

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

    def switch_check_box(self, check_box, *args):
        if check_box == self.chx_box_iterations and check_box.active:
            self.chx_box_iterations.active = True
            self.ids.lblFinishValue.text = 'Max Iterations'
            self.ids.tinFinishValue.text = ''
            self.chx_box_time.active = False
        elif check_box == self.chx_box_time and check_box.active:
            self.chx_box_time.active = True
            self.ids.lblFinishValue.text = 'Time Limit (min)'
            self.ids.tinFinishValue.text = ''
            self.chx_box_iterations.active = False
        if check_box == self.chx_box_iterations and not check_box.active:
            self.chx_box_iterations.active = True
            self.chx_box_time.active = False
        elif check_box == self.chx_box_time and  not check_box.active:
            self.chx_box_iterations.active = False
            self.chx_box_time.active = True
            


    def event(self, *args):
        self.event = Clock.schedule_interval(self.show_progress, 0.025)
    
    def events_cencel(self, *args):
        self.event.cancel()
