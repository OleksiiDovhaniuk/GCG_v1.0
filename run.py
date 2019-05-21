# general imports
import kivy
kivy.require('1.10.1')
import string

# kivy lib imports
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot

# own classes imports
from fileWork import FileWork
from process import Process

# UI of Run Screen
Builder.load_string('''
#:import MeshLinePlot kivy.garden.graph.MeshLinePlot
#:import hex kivy.utils.get_color_from_hex

<RunScreen>:
    name: "RunScreen"
    on_enter: root.go()
    GridLayout:
        cols: 1
        ActionBar:
            size: (100, 40)
            size_hint: (1, None)
            pos_hint: {'top':1}
            background_image: 'res/images/bg_normal.png'
            background_color: hex('#161b1e')
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'GCG v1.0'
                    with_previous: True
                    on_release:
                        root.cansel()
                        root.manager.transition.direction = 'right'
                        root.manager.transition.duration = .30
                        root.manager.current = 'HomeScreen'
                ActionGroup:
                    text: 'File' 
                    mode: 'spinner'
                    size_hint: (0.3, 1)
                    
                    UbuntuActBtn:
                        id: btSetFunction
                        text: "Configurations"
                        background_color: hex('#b7e3ff')
                        on_release:
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30
                            root.manager.current = 'ConfigurationsScreen'
                    UbuntuActBtn:
                        id: btSetTruthTable
                        text: "Set Truth Table"
                        background_color: hex('#b7e3ff')
                        on_release:   
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30           
                            root.manager.current = 'TruthTableScreen'
                    UbuntuActBtn:
                        id: btnExit
                        text: "Exit"
                        background_color: hex('#b7e3ff')
                        color: hex('#d14d70')
                        on_release: app.stop() 
                
                UbuntuActBtn:
                    id: btRun
                    text: "Save Result"
                    color: hex('#74f0f7')
                    size_hint: (0.3, 1)
                    on_release:
                        root.manager.transition.direction = 'left'
                        root.manager.transition.duration = .30
                        root.manager.current = 'RunScreen'
                UbuntuActBtn:
                    id: btCancelRun
                    text: "Cancel"
                    # background_color: hex('#b7e3ff')
                    color: hex('#f9ebac')
                    on_release: root.cansel()
                
        BoxLayout:
            orientation: 'horizontal'
            spacing: 15
            padding: 15
            BoxLayout:
                size: (40, 100)
                size_hint:(None, 1)
                orientation: 'vertical'
                spacing: 5
                padding: 0
                UbuntuLbl:
                    id: lblMaxFF
                    size: (45, 0)
                    size_hint: (1, None)
                    color: hex("#aab6b7")
                    color: (1, 0, 0, 0.7)
                UbuntuLbl:
                    id: lblXaxLalble
                    text: "Fitness Function Values"
                    color: hex("#aab6b7")
                    size: (15, 100)
                    size_hint: (None, 1)
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    canvas.before:
                        PushMatrix
                        Rotate:
                            angle: 90
                            origin: self.center
                    canvas.after:
                        PopMatrix
                UbuntuLbl:
                    id: lblMinFF
                    size: (45, 35)
                    size_hint: (1, None)
                    color: (0, 1, 0, 0.7)
            BoxLayout:
                orientation: 'vertical'
                spacing: 5
                Graph:
                    id: grph
                    xlable: "Generation"
                    ylable: "Fitness function value"
                    y_ticks_major: 1000
                    x_grid_lable: True
                    y_grid_lable: True
                    padding: 1
                    x_grid_lable: True
                    y_grid_lable: True
                BoxLayout:
                    size: (50, 15)
                    size_hint: (1, None)
                    orientation: 'horizontal'
                    padding: -1
                    UbuntuLbl:
                        id: lblZeroIteration
                        size: (5, 15)
                        size_hint: (None, None)
                        text: "0"
                        color: hex("#aab6b7")
                    UbuntuLbl:
                        id: lblXaxLalble
                        text: "Iterations"
                        color: hex("#aab6b7")
                    UbuntuLbl:
                        id: lblCurrentIteration
                        size: (5, 15)
                        size_hint: (None, None)
                        color: hex("#aab6b7")
            FloatLayout:
                size: (75, 100)
                size_hint:(None, 1)
                UbuntuLbl:
                    id: lblCurrentMax
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (1, 0, 0, 0.7)
                    pos_hint: {'x':0.3, 'y':0.8}
                UbuntuLbl:
                    id: lblCurrentAverage
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (0, 0, 1, 0.7)
                    pos_hint: {'x':0.3, 'y':0.5}
                UbuntuLbl:
                    id: lblCurrentMin
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (0, 1, 0, 0.7)
                    pos_hint: {'x':0.3, 'y':0.2}
        BoxLayout:
            orientation: 'horizontal'
            size: (100, 50)
            size_hint:(1, None)
            padding: 30
            BoxLayout:
                orientation: 'horizontal'
                CheckBox:
                    id: chbxMaxPlot
                    active: True
                    size: (20, 30)
                    size_hint:(None, 1)
                UbuntuActBtn:
                    id: lblMaxPlot
                    text: "Max FF Values"
                    color: (1, 0, 0, 0.7)
            BoxLayout:
                orientation: 'horizontal'
                CheckBox:
                    id: chbxAveragePlot
                    active: True
                    size: (20, 30)
                    size_hint:(None, 1)
                UbuntuActBtn:
                    id: lblAveragePlot
                    text: "Average FF Values"
                    color: (0, 0, 1, 0.7)
            BoxLayout:
                orientation: 'horizontal'
                CheckBox:
                    id: chbxMaxPlot
                    active: True
                    size: (20, 30)
                    size_hint:(None, 1)
                UbuntuActBtn:
                    id: lblMinPlot
                    text: "Min FF Values"
                    color: (0, 1, 0, 0.7)
        BoxLayout:
            size: (400, 150)
            size_hint: (1, None)
            ScrollView:
                id:scroller
                TextInput:
                    id: tinResult
                    multiline: True
                    size_hint: (None, None)
                    width: scroller.width
                    height: max(self.minimum_height, scroller.height)
                    font_size: '12sp'
                    cursor_color: [255,255,255,1]
                    background_color: (.17, .18, .17, 1)
                    foreground_color:[255,255,255,1]
                    selection_color: (1,1,1,0.125)

        BoxLayout:
            size: (400, 30)
            size_hint: (1, None)
            spacing: 0
            padding: 10
            UbuntuLbl:
                size:(50, 15)
                size_hint: (None, None)
                id:lblProgress
                text: "0%"

            ProgressBar:
                id: pbProcess
                padding: 100
                max: 1

''')

class RunScreen(Screen):
    """
    The class works with run screen window. 
    """
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)
        self.refresh_process_trigger = Clock.create_trigger(self.refresh_process)
        # Min plot is GREEN
        self.plotMin = MeshLinePlot(color=[0, 1, 0, 0.7])
        # Max plot is RED
        self.plotMax = MeshLinePlot(color=[1, 0, 0, 0.7])
        # Average plot is BLUE
        self.plotAverage = MeshLinePlot(color=[0, 0, 1, 1])

        self.iteration = -1

    def go(self):
        self.ids.grph.add_plot(self.plotMin)
        self.ids.grph.add_plot(self.plotMax)
        self.ids.grph.add_plot(self.plotAverage)
        self.ids.grph.xmax = 1
        
        self.update_Configurations()
        for _ in range (self.generations_number):
            self.refresh_process_trigger()

    def show_results(self):
        self.process.set_winnerResult()
        str_result = ''
        if self.process.winnerGene is None:
            self.ids.tinResult.text = str('The attempt has been failed')
        else:
            print_result = self.process.winnerGene
            for i in range (len(print_result[0])):
                for j in range (len(print_result)):
                    str_result += str(print_result[j][i]) + ' '
                if i < len(print_result[0]) - 1:
                    str_result += '\n'
            self.ids.tinResult.text = str_result
            self.ids.tinResult.text += '\nFitness function value equal: ' + str(round(self.process.winnerResult, 12))
        
    def refresh_process(self, dt):
        self.process.go()
        if self.ids.pbProcess.value < 1:
            # Change progress bar value genetic algorithm progress
            self.ids.pbProcess.value += self.step  
            # Change digit text, that shows percentage of the algorithm completing 
            self.ids.lblProgress.text = str(round(self.ids.pbProcess.value * 100)) + '%'
            # Change fitness function progress bar value 
            self.plotMin.points = [(x, y * 10000) for x, y in enumerate(self.process.minResult_list)] 
            self.plotMax.points = [(x, y * 10000) for x, y in enumerate(self.process.maxResult_list)] 
            self.plotAverage.points = [(x, y * 10000) for x, y in enumerate(self.process.averageResult_list)] 
            
            # Change digit of fitness function on the process
            
            self.ids.lblCurrentMin.text = str(round(self.process.current_minResult, 6))
            self.ids.lblCurrentMin.pos_hint[1] = self.process.current_minResult 
            self.ids.lblCurrentAverage.text = str(round(self.process.current_averageResult, 6))
            self.ids.lblCurrentMin.pos_hint[1] = self.process.current_averageResult
            self.ids.lblCurrentMax.text = str(round(self.process.current_maxResult, 6))
            self.ids.lblCurrentMin.pos_hint[1] = self.process.current_maxResult
            # dinamic graph scope changing 
            self.ids.grph.xmax += 1
            self.ids.grph.ymax = self.process.maxResult * 10000
            if self.process.maxResult == self.process.minResult:
                self.ids.grph.ymin = self.process.minResult * 10000 - 1
            else:
                self.ids.grph.ymin = self.process.minResult * 10000
            # graph min/max numbers update
            self.ids.lblMinFF.text = str(round(self.process.minResult, 4))
            self.ids.lblMaxFF.text = str(round(self.process.maxResult, 4))
            #count iteration
            self.iteration += 1
            self.ids.lblCurrentIteration.text = str(self.iteration)
            
            # Call trigger for refreshing run screen 
            self.refresh_process_trigger()
        else:
            self.show_results()

    def cansel_to_run(self):
        self.ids.btCancelRun.text = "Run"


    def run_to_cansel(self):
        self.ids.btCancelRun.text = "Cansel"


    def cansel(self):
        Clock.unschedule(self.refresh_process_trigger)

        self.ids.tinResult.text = ''
        self.ids.lblProgress.text = '0%'
        self.ids.pbProcess.value = 0
        self.process = None

        # remove all plots
        self.ids.grph.remove_plot(self.plotMin)
        self.ids.grph.remove_plot(self.plotMax)
        self.ids.grph.remove_plot(self.plotAverage)
        # restart graph atributes 
        self.iteration = -1

    def update_Configurations(self):
        fileWork = FileWork() 

        generations_number = fileWork.get_generationNumber()
        ins_list = fileWork.get_insValues()
        outs_list = fileWork.get_outsValues()
        # for x in ins_list:
        #     print(str(x))
        # for x in outs_list:
        #     print(str(x))
        print('-------------')
        insNumber = len(ins_list[0])
        outsNumber = len(outs_list[0])
        # print('insNumber:' + str(insNumber) + ';outsNumber:' + str(outsNumber))
        emptyInputs_value = 1

        generation_size = fileWork.get_generationSize()
        genes_number = fileWork.get_genesNumber()
        noneNode_chance = 0.28571
        crossing_chance = fileWork.get_crossingChance()
        mutation_chance = fileWork.get_mutationChance()
        fitness_coefs = fileWork.get_coefficients()
        self.process = Process(generations_number, emptyInputs_value,generation_size, 
            genes_number, noneNode_chance, crossing_chance, mutation_chance, ins_list, outs_list, fitness_coefs)
        self.generations_number = self.process.generations_number
        self.step = 1 / generations_number
        
        self.ids.grph.x_ticks_major = self.generations_number // 10
