import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from file_work import FileWork
import process

Builder.load_string('''
<TruthTableScreen>:
    # on_enter: root.show_progress()
    GridLayout:
        cols: 2
        padding: 50
        spacing: 10

        UbuntuLbl:
            id: lblInputSignals
            text: "Input Signals"
        UbuntuTxtIn:
            id: tinInputSignals
            multiline: False

        UbuntuLbl:
            id: lblOutputSignals
            text: "Output Signals"
        UbuntuTxtIn:
            id: tinOutputSignals
            multiline: False

        UbuntuLbl:
            id: lblInputValues
            text: "Input Values"
        UbuntuTxtIn:
            id: tinInputValues
            multiline: True

        UbuntuLbl:
            id: lblOutputValues
            text: "Output Values"
        UbuntuTxtIn:
            id: tinOutputValues
            multiline: True

        UbuntuBtn:
            id: btSaveToFile
            text: "Save"
            on_press:
                root.save_truthTable()
        
        UbuntuBtn:
            id: btHome
            text: "Back"
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = .30
                root.manager.current = 'ActionScreen'
 
        BoxLayout:
            size: (400, 30)
            size_hint: (1, None)
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
        self.fileWork = FileWork() 
        self.ids.tinInputSignals.text = self.fileWork.str_insNames()
        self.ids.tinOutputSignals.text = self.fileWork.str_outsNames()
        self.ids.tinInputValues.text = self.fileWork.str_insValues()
        self.ids.tinOutputValues.text = self.fileWork.str_outsValues()

    def save_truthTable(self):
        inputNames = self.ids.tinInputSignals.text
        outputNames = self.ids.tinOutputSignals.text
        inputValues = self.ids.tinInputValues.text
        outputValues = self.ids.tinOutputValues.text
        self.fileWork.save_truthTable(inputNames, outputNames, inputValues, outputValues)

    def show_progress(self):
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