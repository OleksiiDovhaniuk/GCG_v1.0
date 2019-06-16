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
import process

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
            background_color: hex('#e3eaea')
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'GGC v1.0'
                    with_previous: True
                    color: (0,0,0,1)
                    on_release:
                        root.cansel()
                        root.manager.transition.direction = 'right'
                        root.manager.transition.duration = .30
                        root.manager.current = 'HomeScreen'
                ActionGroup:
                    text: 'File' 
                    mode: 'spinner'
                    size_hint: (0.3, 1)
                    color: (0,0,0,1)
                    
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
                        color: hex('#0e7c7c')
                        on_release: app.stop() 
                
                UbuntuActBtn:
                    id: btRun
                    text: "Save Result"
                    color: hex('#0e7c7c')
                    size_hint: (0.3, 1)
                    on_release:
                        root.manager.transition.direction = 'left'
                        root.manager.transition.duration = .30
                        root.manager.current = 'RunScreen'
                UbuntuActBtn:
                    id: btCancelRun
                    text: "Cancel"
                    # background_color: hex('#b7e3ff')
                    color: hex('#b53b3b')
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
                    color: hex("#2d2d2d")
                UbuntuLbl:
                    id: lblXaxLalble
                    text: "Fitness Function Values"
                    color: hex("#2d2d2d")
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
                    color: hex('#2d2d2d')
            BoxLayout:
                orientation: 'vertical'
                spacing: 5
                Graph:
                    id: grph
                    y_ticks_major: 1000
                    x_grid_lable: True
                    y_grid_lable: True
                    padding: 1
                    x_grid_lable: True
                    y_grid_lable: True
                    background_color: hex('#e3eaea')
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
                        color: hex("#2d2d2d")
                    UbuntuLbl:
                        id: lblXaxLalble
                        text: "Iterations"
                        color: hex("#2d2d2d")
                    UbuntuLbl:
                        id: lblCurrentIteration
                        size: (5, 15)
                        size_hint: (None, None)
                        color: hex("#2d2d2d")
            FloatLayout:
                size: (75, 100)
                size_hint:(None, 1)
                UbuntuLbl:
                    id: lblCurrentMax
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (0.8, 0, 0, 1)
                    pos_hint: {'x':0.3, 'y':0.8}
                UbuntuLbl:
                    id: lblCurrentAverage
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (0, 0, 1, 1)
                    pos_hint: {'x':0.3, 'y':0.5}
                UbuntuLbl:
                    id: lblCurrentMin
                    size: (5, 15)
                    size_hint: (None, None)
                    color: (0, 0.7, 0, 1)
                    pos_hint: {'x':0.3, 'y':0.2}
        # BoxLayout:
        #     orientation: 'horizontal'
        #     size: (100, 50)
        #     size_hint:(1, None)
        #     padding: 30
        #     BoxLayout:
        #         orientation: 'horizontal'
        #         CheckBox:
        #             id: chbxMaxPlot
        #             active: True
        #             size: (20, 30)
        #             size_hint:(None, 1)
        #         UbuntuActBtn:
        #             id: lblMaxPlot
        #             text: "Max FF Values"
        #             color: (0.8, 0, 0, 1)
        #     BoxLayout:
        #         orientation: 'horizontal'
        #         CheckBox:
        #             id: chbxAveragePlot
        #             active: True
        #             size: (20, 30)
        #             size_hint:(None, 1)
        #         UbuntuActBtn:
        #             id: lblAveragePlot
        #             text: "Average FF Values"
        #             color: (0, 0, 1, 1)
        #     BoxLayout:
        #         orientation: 'horizontal'
        #         CheckBox:
        #             id: chbxMaxPlot
        #             active: True
        #             size: (20, 30)
        #             size_hint:(None, 1)
        #         UbuntuActBtn:
        #             id: lblMinPlot
        #             text: "Min FF Values"
        #             color: (0, 0.7, 0, 1)
        BoxLayout:
            size: (400, 150)
            size_hint: (1, None)
            UbuntuTxtIn:
                id: tinResult
                multiline: True
                halign: 'center'
                font_size: 14
                font_color: (1,1,1,1)
                cursor_color: [0,0,0,1]
                background_color: hex('#e3eaea')

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
            
            UbuntuLbl:
                size:(100, 15)
                size_hint: (None, None)
                id:lblClock
                text: "00:00:00"

''')

class RunScreen(Screen):
    """
    The class works with run screen window. 
    """
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)
        self.refresh_process_trigger = Clock.create_trigger(self.refresh_process)
        # Min plot is GREEN
        self.plotMin = MeshLinePlot(color=[0, 0.7, 0, 1])
        # Max plot is RED
        self.plotMax = MeshLinePlot(color=[0.8, 0, 0, 1])
        # Average plot is BLUE
        self.plotAverage = MeshLinePlot(color=[0, 0, 1, 1])

    def go(self):
        self.ids.grph.add_plot(self.plotMin)
        self.ids.grph.add_plot(self.plotMax)
        self.ids.grph.add_plot(self.plotAverage)
        self.ids.grph.xmax = 1
        
        self.update_Configurations()
        # self.clock_event = Clock.schedule_interval(self.clock_update, 1)
        for _ in range (process.generations_number):
            self.refresh_process_trigger()

    def show_results(self):
        str_result = 'Best result:\n'
        str_result += self.result_to_str(process.best_chromosome, \
            process.absolute_max_ff, process.time_to_find) + '\n\n'
        if process.iteration == process.generations_number:
            if process.results['chromosome']:
                str_result += 'Other results:\n'
            for index in range (len(process.results['chromosome'])):
                str_result += f'Result #{str(index + 1)}\n'
                str_result += self.result_to_str(
                    process.results['chromosome'][index],
                    process.results['fitness_function'][index],
                    process.results['time'][index])
                
                if index < len(process.results['time']) - 1:
                    str_result += '\n\n'
        self.ids.tinResult.text = str_result

    def result_to_str(self, chromosome, fitness_function_value, time):
        """ Convert result of complex type (3D list, float, str) to string.
        """
        str_result = ''
        for i in range(len(chromosome[0])):
            for j in range(len(chromosome)):
                str_result += str(chromosome[j][i]) + ' '
            str_result += '\n'
        str_result += 'Fitness function value equal:' + \
            f' {str(round(fitness_function_value, 8))}, that took '
        if time[:2] != '00':
            if time[0] == '0':
                str_result += f'{time[1]} hour'
            else:
                str_result += f'{time[:2]} hour'
            if time[:2] != '01':
                str_result += 's'
            str_result += ' '
        if time[3:5] != '00':
            if time[3] == '0':
                str_result += f'{time[4]} minute'
            else:
                str_result += f'{time[3:5]} minute'
            if time[3:5] != '01':
                str_result += 's'
            str_result += ' '
        if time[6] == '0':
            str_result += f'{time[7]} second'
        else:
            str_result += f'{time[6:8]} second'
        if time[6:8] != '01':
            str_result += 's'
        str_result += '.'

        return str_result

    def refresh_process(self, dt):
        process.go()
        self.show_results()
        if process.iteration < process.generations_number:
            # Change progress bar value genetic algorithm progress
            self.ids.pbProcess.value += process.progress_step
            # Change digit text, that shows percentage of the algorithm completing 
            self.ids.lblProgress.text = str(round(self.ids.pbProcess.value * 100)) + '%'
            # Change fitness function progress bar value 
            self.plotMax.points = [(x, y * 10000) for x, y in enumerate(process.max_ffs)] 
            self.plotAverage.points = [(x, y * 10000) for x, y in enumerate(process.average_ffs)] 
            self.plotMin.points = [(x, y * 10000) for x, y in enumerate(process.min_ffs)] 
            
            # Change digit of fitness function on the process
            
            self.ids.lblCurrentMax.text = str(round(process.max_ff, 6))
            self.ids.lblCurrentAverage.text = str(round(process.average_ff, 6))
            self.ids.lblCurrentMin.text = str(round(process.min_ff, 6))
            # dinamic graph scope changing 
            self.ids.grph.xmax = process.iteration
            self.ids.grph.ymax = process.absolute_max_ff * 10000
            if process.absolute_max_ff == process.absolute_min_ff:
                self.ids.grph.ymin = process.absolute_min_ff * 10000 - 1
            else:
                self.ids.grph.ymin = process.absolute_min_ff * 10000
            # graph min/max numbers update
            self.ids.lblMaxFF.text = str(round(process.absolute_max_ff, 4))
            self.ids.lblMinFF.text = str(round(process.absolute_min_ff, 4))
            # count iteration
            self.ids.lblCurrentIteration.text = str(process.iteration + 1)
            # show progress time
            self.ids.lblClock.text = process.time
            self.refresh_process_trigger()
        else:
            # set progress bar as full
            self.ids.pbProcess.value = 1
            self.ids.lblProgress.text = '100%'

    def cansel_to_run(self):
        self.ids.btCancelRun.text = "Run"


    def run_to_cansel(self):
        self.ids.btCancelRun.text = "Cansel"


    def cansel(self):
        Clock.unschedule(self.refresh_process_trigger)
        # Clock.unschedule(self.clock_event)

        self.ids.tinResult.text = ''
        self.ids.lblProgress.text = '0%'
        self.ids.lblClock.text = '00:00:00'
        self.ids.pbProcess.value = 0

        # remove all plots
        self.ids.grph.remove_plot(self.plotMin)
        self.ids.grph.remove_plot(self.plotMax)
        self.ids.grph.remove_plot(self.plotAverage)

    def update_Configurations(self):
        import process
        self.ids.grph.x_ticks_major = process.generations_number // 10
