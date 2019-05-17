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

        Label:
            id: lblInputSignals
            text: "Input Signals"
        TextInput:
            id: tinInputSignals
            multiline: False

        Label:
            id: lblOutputSignals
            text: "Output Signals"
        TextInput:
            id: tinOutputSignals
            multiline: False

        Label:
            id: lblInputValues
            text: "Input Values"
        TextInput:
            id: tinInputValues
            multiline: True

        Label:
            id: lblOutputValues
            text: "Output Values"
        TextInput:
            id: tinOutputValues
            multiline: True

        Button:
            id: btSaveToFile
            text: "Save"
            on_press:
                root.save_truthTable()
        
        Button:
            id: btRun
            text: "Run"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = .30
                root.manager.current = 'RunScreen'

        Button:
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