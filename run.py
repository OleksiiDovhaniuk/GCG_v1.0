import kivy
kivy.require('1.10.1')
import string

# kivy lib import
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

# own classes import
from fileWork import FileWork
from process import Process

# UI of Run Screen
Builder.load_string('''
<RunScreen>:
    name : "RunScreen"
    on_enter: root.go()
    GridLayout:
        cols: 2
        padding: 50
        spacing: 10

        Button:
            id: btRun
            text: "Save Result"

        Button:
            id: btCancel
            text: "Cancel"
            
            on_release:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = .30
                root.manager.current = 'HomeScreen'
                root.cansel()
        
        ScrollView:
            id:scroller
            TextInput:
                id: tinResult1
                text: "Result1"
                multiline: True
                size_hint: (None, None)
                width: scroller.width
                height: max(self.minimum_height, scroller.height)
                font_size: '12sp'
                cursor_color: [255,255,255,1]
                background_color: (.17, .18, .17, 1)
                foreground_color:[255,255,255,1]
                selection_color: (1,1,1,0.125)

        Label:
            id:lblResult2
            text: "Result2"

        ProgressBar:
            id: pbProcess
            max: 1

        Label:
            id:lblProgress
            text: "0%"

        ProgressBar:
            id: pbFitnessFunction
            foreground_color: (.53, .15, .15, 1)
            max: 1
        # Plot:
        #     id: pltFitnessFunction
        #     xlabel: "Generation"
        #     ylabel: "Fitness Function Values"

        Label:
            id:lblFitnessFunction
            text: "0%"
''')

class RunScreen(Screen):
    """
    The class works with run screen window. 
    """
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)
        self.refresh_process_trigger = Clock.create_trigger(self.refresh_process)
        self.update_Configurations()
        
    def go(self):
        self.update_Configurations()
        for _ in range (self.generations_number):
            self.refresh_process_trigger()

    def show_results(self):
        self.process.set_winnerResult()
        str_result = ''
        if self.process.winnerGene is None:
            self.ids.tinResult1.text = str(None)
            self.ids.lblResult2.text = str('The attempt has been failed')
        else:
            print_result = self.process.winnerGene
            for i in range (len(print_result[0])):
                for j in range (len(print_result)):
                    str_result += str(print_result[j][i]) + ' '
                if i < len(print_result[0]) - 1:
                    str_result += '\n'
            self.ids.tinResult1.text = str_result
            self.ids.lblResult2.text = str(round(self.process.winnerResult, 8))
        
    def refresh_process(self, dt):
        self.process.go()
        if self.ids.pbProcess.value < 1:
            # Change progress bar value genetic algorithm progress
            self.ids.pbProcess.value += self.step  
            # Change digit text, that shows percentage of the algorithm completing 
            self.ids.lblProgress.text = str(round(self.ids.pbProcess.value * 100)) + '%'

            # Change fitness function progress bar value 
            self.ids.pbFitnessFunction.value = self.process.current_averageResult
            # Change digit of fitness function on the process
            self.ids.lblFitnessFunction.text = str(round(self.process.current_averageResult, 8))

            # Call trigger for refreshing run screen 
            self.refresh_process_trigger()
        else:
            self.show_results()

    def cansel(self):
        Clock.unschedule(self.refresh_process_trigger)
        self.ids.tinResult1.text = "Result1"
        self.ids.lblResult2.text = "Result2"
        self.ids.lblProgress.text = "0%"
        self.ids.pbProcess.value = 0
        self.ids.lblFitnessFunction.text = "0"
        self.ids.pbFitnessFunction.value = 0
        self.process.current_averageResult = None
        self.process.generation = None

    def update_Configurations(self):
        fileWork = FileWork() 

        generations_number = fileWork.get_generationNumber()
        ins_list = fileWork.get_insValues()
        outs_list = fileWork.get_outsValues()
        insNumber = len(ins_list[0])
        outsNumber = len(outs_list[0])
        # print('insNumber:' + str(insNumber) + ';outsNumber:' + str(outsNumber))
        emptyInputs_value = 1

        generation_size = fileWork.get_generationSize()
        genes_number = fileWork.get_genesNumber()
        noneNode_chance = 0.5
        crossing_chance = fileWork.get_crossingChance()
        mutation_chance = fileWork.get_mutationChance()
        fitness_coefs = fileWork.get_coefficients()

        self.process = Process(generations_number, insNumber, outsNumber, emptyInputs_value,generation_size, 
            genes_number, noneNode_chance, crossing_chance, mutation_chance, ins_list, outs_list, fitness_coefs)
        self.generations_number = self.process.generations_number
        self.step = 1 / generations_number