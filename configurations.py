import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from fileWork import FileWork

Builder.load_string('''
<ConfigurationsScreen>:
    GridLayout:
        cols: 2
        padding: 50
        spacing: 10

        UbuntuLbl:
            id: lblGenerationNumber
            text: "Generation Number"
        TextInput:
            id: tinGenerationNumber
            multiline: False

        UbuntuLbl:
            id: lblGenerationSize
            text: "Generation Size"
        TextInput:
            id: tinGenerationSize
            multiline: True

        UbuntuLbl:
            id: GenesNumber
            text: "Genes Number"
        TextInput:
            id: tinGenesNumber
            multiline: False

        UbuntuLbl:
            id: lblCoefficients
            text: "Coefficients"
        TextInput:
            id: tinCoefficients
            multiline: True

        UbuntuLbl:
            id: lblCrossing
            text: "Crossover Chance"
        TextInput:
            id: tinCrossing
            multiline: True

        UbuntuLbl:
            id: lblMutation
            text: "Mutation Chance"
        TextInput:
            id: tinMutation
            multiline: True

        UbuntuBtn:
            id: btSaveToFile
            text: "Save"
            on_press:
                root.save_configurations()
        
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

class ConfigurationsScreen(Screen):

    def __init__(self, **kwargs):
        super(ConfigurationsScreen, self).__init__(**kwargs)
        self.fileWork = FileWork() 
        self.ids.tinGenerationNumber.text = self.fileWork.str_generationNumber()
        self.ids.tinGenerationSize.text = self.fileWork.str_generationSize()
        self.ids.tinGenesNumber.text = self.fileWork.str_genesNumber()
        self.ids.tinCoefficients.text = self.fileWork.str_coefficients()
        self.ids.tinCrossing.text = self.fileWork.str_crossingChance()
        self.ids.tinMutation.text = self.fileWork.str_mutationChance()

    def save_configurations(self):
        generation_number = self.ids.tinGenerationNumber.text
        generation_size = self.ids.tinGenerationSize.text
        genes_number = self.ids.tinGenesNumber.text
        crossing_chance = self.ids.tinCrossing.text
        mutation_chance = self.ids.tinMutation.text
        fitnessFunction_coefficients = self.ids.tinCoefficients.text
        self.fileWork.save_configurations(generation_number, generation_size, 
        genes_number, crossing_chance, mutation_chance, fitnessFunction_coefficients)