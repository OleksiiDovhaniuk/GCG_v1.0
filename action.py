# general imports
import string

import kivy
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot
# kivy lib imports
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen

import process
# own classes imports
from home import UbuntuBtn

kivy.require('1.10.1')



# UI of Run Screen
Builder.load_string('''
#:import MeshLinePlot kivy.garden.graph.MeshLinePlot
#:import hex kivy.utils.get_color_from_hex

<ActionScreen>:
    name: "ActionScreen"
    on_enter: 
        dropdown_file.dismiss(self)
        dropdown_action.dismiss(self)
        dropdown_info.dismiss(self)
        root.go()
    GridLayout:
        cols: 1
        BoxLayout:
            id: bxlt_menu_bar
            orientation: 'horizontal'
            size_hint: (1, None)
            size: (30, 35)
            canvas.before:
                Color:
                    rgb: utils.get_color_from_hex('#b2b2b2')
                Rectangle:
                    pos: self.pos
                    size: self.size
            UbuntuBtn:
                id: btn_file
                text: 'File'
                on_release: dropdown_file.open(self)
                DropDown:
                    id: dropdown_file
            UbuntuBtn:
                id: btn_action
                text: 'Action'
                on_release: dropdown_action.open(self)
                DropDown:
                    id: dropdown_action
            UbuntuBtn:
                id: btn_info
                text: 'Info'
                on_release: dropdown_info.open(self)
                DropDown:
                    id: dropdown_info
        BoxLayout:
            orientation: 'horizontal'
            spacing: 15
            padding: 15

            BoxLayout:
                size_hint:(None, 1)
                size: (20, 100)
                orientation: 'vertical'
                spacing: 5
                padding: 0
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
            BoxLayout:
                size_hint:(None, 1)
                size: (20, 100)
                orientation: 'vertical'
                UbuntuLbl:
                    id: lblMaxFF
                    size_hint: (1, None)
                    size: (45, 0)
                    color: hex("#2d2d2d")
                BoxLayout:
                    size_hint: (1, 1)
                    UbuntuLbl:
                        id: lblAbsoluteMaxFF
                        pos_hint:{"top":0.5}
                        size: (45, 0)
                        color: hex("#2d2d2d")
                    UbuntuLbl:
                        size_hint: (1, 1)
                        color: hex("#2d2d2d")
                    UbuntuLbl:
                        id: lblAbsoluteMinFF
                        pos_hint:{"bottom":0.5}
                        size: (45, 0)
                        color: hex("#2d2d2d")
                UbuntuLbl:
                    id: lblMinFF
                    size_hint: (1, None)
                    size: (45, 35)
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
            BoxLayout:
                orientation: 'vertical'
                size_hint:(None, 1)
                size: (75, 100)
                UbuntuLbl:
                    id: lblCurrentMax
                    color: (0.8, 0, 0, 1)
                UbuntuLbl:
                    id: lblCurrentAverage
                    color: (0, 0, 1, 1)
                UbuntuLbl:
                    id: lblCurrentMin
                    color: (0, 0.7, 0, 1)
        BoxLayout:
            orientation: 'horizontal'
            size_hint:(1, .2)
            size: (300, 30)
            spacing: 50
            padding: 20
            pos_hint: {'center_x': 0.5}
            ClearBtn:
                orientation: 'horizontal'
                size_hint:(None, 1)
                size: (135, 30)
                CheckBox:
                    id: chbxMaxPlot
                    active: True
                    size_hint: (None, 1)
                    size: (5, 10)
                UbuntuLbl:
                    id: lblMaxPlot
                    text: "Max FF Values"
                    color: (0, 0, 0, 1)
            ClearBtn:
                size_hint:(None, 1)
                size: (170, 30)
                orientation: 'horizontal'
                CheckBox:
                    id: chbxAveragePlot
                    active: True
                    size_hint: (None, 1)
                    size: (5, 10)
                UbuntuLbl:
                    id: lblAveragePlot
                    text: "Average FF Values"
                    color: (0, 0, 0, 1)
            ClearBtn:
                size_hint:(None, 1)
                size: (130, 30)
                orientation: 'horizontal'
                CheckBox:
                    id: chbxMinPlot
                    active: True
                    size_hint: (None, 1)
                    size: (5, 10)
                UbuntuLbl:
                    id: lblMinPlot
                    text: "Min FF Values"
                    color: (0, 0, 0, 1)
            ClearBtn:
                size_hint:(None, 1)
                size: (145, 30)
                orientation: 'horizontal'
                CheckBox:
                    id: chbxDynamic
                    active: True
                    size_hint: (None, 1)
                    size: (30, 10)
                UbuntuLbl:
                    id: lblDynamic
                    text: "Dynamic Plot"
                    color: (0, 0, 0, 1)
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

class ActionScreen(Screen):
    """
    The class works with run screen window. 
    """

    def __init__(self, **kwargs):
        super(ActionScreen, self).__init__(**kwargs)
        self.refresh_process_trigger = Clock.create_trigger(self.refresh_process)
        # Min plot is GREEN
        self.plotMin = MeshLinePlot(color=[0, 0.7, 0, 1])
        # Max plot is RED
        self.plotMax = MeshLinePlot(color=[0.8, 0, 0, 1])
        # Average plot is BLUE
        self.plotAverage = MeshLinePlot(color=[0, 0, 1, 1])
        # dropdown_file
        self.btn_configurations = UbuntuBtn(id="btn_configurations", text="Configurations", \
            on_release=self.manage_to_configurations)
        self.btn_truth_table = UbuntuBtn(id="btn_truth_table", text="Truth table", \
            on_release=self.manage_to_truth_table)
        self.btn_save = UbuntuBtn(id="btn_save", text="Save job")
        self.btn_load = UbuntuBtn(id="btn_load", text="Load job")
        self.btn_exit = UbuntuBtn(id="btn_exit", text="Exit", \
            on_release=quit)
        self.ids.dropdown_file.add_widget(self.btn_configurations)
        self.ids.dropdown_file.add_widget(self.btn_truth_table)
        self.ids.dropdown_file.add_widget(self.btn_save)
        self.ids.dropdown_file.add_widget(self.btn_load)
        self.ids.dropdown_file.add_widget(self.btn_exit)
        # dropdown_action
        self.btn_new_start = UbuntuBtn(id="btn_new_start", text="New Start", \
            on_release=self.manage_new_start)
        self.btn_pause_continue = UbuntuBtn(id="btn_pause_continue", text="Pause", \
            on_release=self.manage_pause_continue)
        self.btn_cancel = UbuntuBtn(id="btn_cancel", text="Cancel", \
            on_release=self.manage_cancel)
        self.ids.dropdown_action.add_widget(self.btn_new_start)
        self.ids.dropdown_action.add_widget(self.btn_pause_continue)
        self.ids.dropdown_action.add_widget(self.btn_cancel)
        # dropdown_info
        self.btn_tutorial = UbuntuBtn(id="btn_tutorial", text="Tutorial")
        self.btn_about = UbuntuBtn(id="btn_about", text="About GGC")
        self.ids.dropdown_info.add_widget(self.btn_tutorial)
        self.ids.dropdown_info.add_widget(self.btn_about)
        
    def go(self):
        if not process.is_paused and process.is_process:
            self.ids.grph.add_plot(self.plotMax)
            self.ids.grph.add_plot(self.plotAverage)
            self.ids.grph.add_plot(self.plotMin)
            self.ids.grph.xmax = 1
            self.ids.chbxDynamic.active = True
            self.ids.chbxDynamic.disabled = False
            self.ids.chbxMaxPlot.disabled = False
            self.ids.chbxAveragePlot.disabled = False
            self.ids.chbxMinPlot.disabled = False
            
            # self.clock_event = Clock.schedule_interval(self.clock_update, 1)
            for _ in range (process.generations_number):
                self.refresh_process_trigger()


    def refresh_process(self, dt):
        process.go()
        self.show_results()
        if process.iteration < process.generations_number:
            # Change progress bar value genetic algorithm progress
            self.ids.pbProcess.value += process.progress_step
            # Change digit text, that shows percentage of the algorithm completing 
            self.ids.lblProgress.text = str(round(self.ids.pbProcess.value * 100)) + '%'
            
            # Change digit of fitness function on the process
            # dinamic graph scope changing 
            if self.ids.chbxDynamic.active:
                self.ids.grph.xmax = process.iteration
                self.ids.grph.ymax = process.absolute_max_ff * 10000
                # count iteration
                self.ids.lblCurrentIteration.text = str(process.iteration + 1)
                # graph min/max numbers update
                self.ids.lblMaxFF.text = str(round(process.absolute_max_ff, 2))
                self.ids.lblMinFF.text = str(round(process.absolute_min_ff, 2))
                if process.absolute_max_ff == process.absolute_min_ff:
                    self.ids.grph.ymin = process.absolute_min_ff * 10000 - 1
                else:
                    self.ids.grph.ymin = process.absolute_min_ff * 10000
                # self.ids.lblAbsoluteMaxFF.text = ''
                # self.ids.lblAbsoluteMinFF.text = ''
            else:
                self.ids.grph.xmax = process.generations_number
                self.ids.grph.ymax = 10000
                self.ids.grph.ymin = 0
                # count iteration
                self.ids.lblCurrentIteration.text = str(process.generations_number)
                # graph min/max numbers update
                self.ids.lblMaxFF.text = str(1)
                self.ids.lblMinFF.text = str(0)

                # self.ids.lblAbsoluteMaxFF.text = str(round(process.absolute_max_ff, 2))
                # self.ids.lblAbsoluteMinFF.text = str(round(process.absolute_min_ff, 2))
            # show max plot values
            if self.ids.chbxMaxPlot.active:
                self.plotMax.points = [(x, y * 10000) for x, y in enumerate(process.max_ffs)] 
                self.ids.lblCurrentMax.text = 'max:\n{}'.format(str(round(process.max_ff, 5)))
            else:
                self.plotMax.points = []
                self.ids.lblCurrentMax.text = ""

            # show average plot values
            if self.ids.chbxAveragePlot.active:
                self.plotAverage.points = [(x, y * 10000) for x, y in enumerate(process.average_ffs)] 
                self.ids.lblCurrentAverage.text = 'average:\n{}'.format(str(round(process.average_ff, 5)))

                if self.ids.chbxDynamic.active:
                    if self.ids.chbxMaxPlot.active and not self.ids.chbxMinPlot.active:
                        self.ids.grph.ymin = min(process.average_ffs) * 10000
                        self.ids.lblMinFF.text = str(round(min(process.average_ffs), 2))
                    elif not self.ids.chbxMaxPlot.active and self.ids.chbxMinPlot.active:
                        self.ids.grph.ymax = max(process.average_ffs) * 10000
                        self.ids.lblMaxFF.text = str(round(max(process.average_ffs), 2))

            else:
                self.plotAverage.points = [] 
                self.ids.lblCurrentAverage.text = ""
            # show min plot values
            if self.ids.chbxMinPlot.active:
                self.plotMin.points = [(x, y * 10000) for x, y in enumerate(process.min_ffs)] 
                self.ids.lblCurrentMin.text = 'min:\n{}'.format(str(round(process.min_ff, 5)))
            else:
                self.plotMin.points = [] 
                self.ids.lblCurrentMin.text = ""

            # show progress time
            self.ids.lblClock.text = process.time
            self.refresh_process_trigger()

            if not self.ids.chbxMaxPlot.active and not self.ids.chbxAveragePlot.active:
                self.ids.chbxMinPlot.active = True
                self.ids.chbxMinPlot.disabled = True
                if self.ids.chbxDynamic.active:
                    self.ids.lblMaxFF.text = str(round(max(process.min_ffs), 2))
                    self.ids.grph.ymax = max(process.min_ffs) * 10000
            elif not self.ids.chbxMaxPlot.active and not self.ids.chbxMinPlot.active:
                self.ids.chbxAveragePlot.active = True
                self.ids.chbxAveragePlot.disabled = True
                if self.ids.chbxDynamic.active:
                    self.ids.lblMaxFF.text = str(round(max(process.average_ffs), 2))
                    self.ids.lblMinFF.text = str(round(min(process.average_ffs), 2))
                    self.ids.grph.ymax = max(process.average_ffs) * 10000
                    self.ids.grph.ymin = min(process.average_ffs) * 10000
            elif not self.ids.chbxAveragePlot.active and not self.ids.chbxMinPlot.active:
                self.ids.chbxMaxPlot.active = True
                self.ids.chbxMaxPlot.disabled = True
                if self.ids.chbxDynamic.active:
                    self.ids.lblMinFF.text = str(round(min(process.max_ffs), 2))
                    self.ids.grph.ymin = min(process.max_ffs) * 10000
            else:
                self.ids.chbxMaxPlot.disabled = False
                self.ids.chbxAveragePlot.disabled = False
                self.ids.chbxMinPlot.disabled = False

        else:
            self.ids.chbxDynamic.active = False
            self.ids.chbxMaxPlot.active = True
            self.ids.chbxAveragePlot.active = True
            self.ids.chbxMinPlot.active = True

            self.ids.chbxDynamic.disabled = True
            self.ids.chbxMaxPlot.disabled = True
            self.ids.chbxAveragePlot.disabled = True
            self.ids.chbxMinPlot.disabled = True

            self.ids.grph.xmax = process.generations_number
            self.ids.grph.ymax = 10000
            self.ids.grph.ymin = 0
            self.ids.lblMaxFF.text = str(round(process.absolute_max_ff, 2))
            self.ids.lblMinFF.text = str(round(process.absolute_min_ff, 2))
            # count iteration
            self.ids.lblCurrentIteration.text = str(process.generations_number)
            # graph min/max numbers update
            self.ids.lblMaxFF.text = str(1)
            self.ids.lblMinFF.text = str(0)

            self.plotMax.points = [(x, y * 10000) for x, y in enumerate(process.max_ffs)] 
            self.ids.lblCurrentMax.text = 'max:\n{}'.format(str(round(process.max_ff, 5)))

            self.plotAverage.points = [(x, y * 10000) for x, y in enumerate(process.average_ffs)] 
            self.ids.lblCurrentAverage.text = 'average:\n{}'.format(str(round(process.average_ff, 5)))

            self.plotMin.points = [(x, y * 10000) for x, y in enumerate(process.min_ffs)] 
            self.ids.lblCurrentMin.text = 'min:\n{}'.format(str(round(process.min_ff, 5)))

            # set progress bar as full
            self.ids.pbProcess.value = 1
            self.ids.lblProgress.text = '100%'
        if self.ids.grph.ymax == self.ids.grph.ymin:
            self.ids.grph.ymax +=1 
        
            
    def new_start(self):
        self.cancel()
        process.new_start()
        self.go()

    def cancel(self):
        Clock.unschedule(self.refresh_process_trigger)

        self.ids.tinResult.text = ''
        self.ids.lblProgress.text = '0%'
        self.ids.lblClock.text = '00:00:00'
        self.ids.pbProcess.value = 0

        # remove all plots
        self.ids.grph.remove_plot(self.plotMin)
        self.ids.grph.remove_plot(self.plotMax)
        self.ids.grph.remove_plot(self.plotAverage)

        process.is_process = False

    def update_Configurations(self):
        
        self.ids.grph.x_ticks_major = process.generations_number // 10

    def manage_to_configurations(self, *args):
        self.ids.dropdown_file.dismiss()
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .30
        self.manager.current = 'ConfigurationsScreen'

    def manage_to_truth_table(self, *args):
        self.ids.dropdown_file.dismiss()
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .30
        self.manager.current = 'TruthTableScreen'

    def manage_new_start(self, *args):
        self.ids.dropdown_action.dismiss()
        if self.ids.pbProcess.value == 0:
            self.ids.dropdown_action.add_widget(self.btn_pause_continue)
            self.ids.dropdown_action.add_widget(self.btn_cancel)
        self.new_start()
        process.is_paused = True
        self.manage_pause_continue()

    def manage_pause_continue(self, *args):
        self.ids.dropdown_action.dismiss()
        if process.is_paused:
            process.is_paused = False
            self.btn_pause_continue.text = 'Pause'
            self.refresh_process_trigger = Clock.create_trigger(self.refresh_process)
            process.resume_time()
            self.go()
        else:
            process.is_paused = True
            self.btn_pause_continue.text = 'Continue'
            Clock.unschedule(self.refresh_process_trigger)
            
    def manage_cancel(self, *args):
        self.ids.dropdown_action.dismiss()
        self.cancel()
        self.ids.dropdown_action.remove_widget(self.btn_pause_continue)
        self.ids.dropdown_action.remove_widget(self.btn_cancel)


    def show_results(self):
        str_result = 'Best result:\n'
        str_result += self.result_to_str(process.best_chromosome, \
            process.absolute_max_ff, process.time_to_find)
        if process.iteration == process.generations_number:
            if process.results['chromosome']:
                str_result += '\n\nOther results:\n'
            for index in range (len(process.results['chromosome'])):
                str_result += 'Result #{}\n'.format(str(index + 1))
                str_result += self.result_to_str(
                    process.results['chromosome'][index],
                    process.results['fitness_function'][index],
                    process.results['time'][index])
                
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
            ' {}, that took '.format(str(round(fitness_function_value, 8)))
        if time[:2] != '00':
            if time[0] == '0':
                str_result += '{} hour'.format(time[1])
            else:
                str_result += '{} hour'.format(time[:2])
            if time[:2] != '01':
                str_result += 's'
            str_result += ' '
        if time[3:5] != '00':
            if time[3] == '0':
                str_result += '{} minute'.format(time[4])
            else:
                str_result += '{} minute'.format(time[3:5])
            if time[3:5] != '01':
                str_result += 's'
            str_result += ' '
        if time[6] == '0':
            str_result += '{} second'.format(time[7])
        else:
            str_result += '{} second'.format(time[6:8])
        if time[6:8] != '01':
            str_result += 's'
        str_result += '.'

        return str_result
