import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from fileWork import FileWork

Builder.load_string('''
<TruthTableScreen>:
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
            id: btRun
            text: "Run"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = .30
                root.manager.current = 'RunScreen'

        UbuntuBtn:
            id: btHome
            text: "Home"
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = .30
                root.manager.current = 'HomeScreen'
 
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