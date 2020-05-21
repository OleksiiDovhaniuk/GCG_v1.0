from datetime import datetime
from functools import partial

import kivy
import matplotlib.pyplot as plot
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import \
    FigureCanvasKivyAgg as Figure
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

import file_work as fw
from control.btn import Btn
from control.dropDownMenu import DropDownMenu
from control.layout import Separator10
from control.lbl import Lbl, ResultsLbl
from control.scheme import Scheme
from control.sideConfigurations import Algorithm, Input, Plot, Results
from design import Design
from process import Process

# engine = KivyEngine()

kivy   .require  ('1.10.1')
Builder.load_file('view/main.kv')

class Main(Screen):
    theme = Design().default_theme
    SCHEME_HEIGHT = 150
    MAX_FONT_SIZE = 16
    HEIGHT_COEFNT = 2
    CLOCK = .01
    RESUL_TIME = 3
    RESULT_NO = 3
    SIDE_CONF_WIDTH = 768

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.side_config_algorithm = Algorithm()
        self.side_config_input = Input()
        self.side_config_plot = Plot()
        self.side_results  = Results()

        self.btn_run = Btn(text='Run')
        self.btn_pause = Btn(text='Pause')
        self.btn_restore = Btn(text='Restore')
        self.btn_stop = Btn(text='Stop')

        self.btn_run.bind(on_release=self.run)
        self.btn_pause.bind(on_release=self.pause)
        self.btn_restore.bind(on_release=self.restore)
        self.btn_stop.bind(on_release=self.stop)

        self.show_config_algorithm()
        self.pause_start = None

    def show_config_algorithm(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = self.SIDE_CONF_WIDTH
        side_cont.add_widget(self.side_config_algorithm)

        self.ids.btn_algorithm.disabled = True
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
        self.ids.btn_results.disabled = False
    
    def show_config_inputs(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = self.SIDE_CONF_WIDTH
        side_cont.add_widget(self.side_config_input)
        
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = True
        self.ids.btn_plot.disabled = False
        self.ids.btn_results.disabled = False
    
    def show_config_plot(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = self.SIDE_CONF_WIDTH
        side_cont.add_widget(self.side_config_plot)

        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = True
        self.ids.btn_results.disabled = False

    def show_side_results(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = self.SIDE_CONF_WIDTH
        side_cont.add_widget(self.side_results)

        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
        self.ids.btn_results.disabled = True

    def minimize_conf(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 0
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
        self.ids.btn_results.disabled = False

    def run(self, *args):
        self.delta_time = datetime.now()
        self.ids.btn_run.clear_widgets()
        self.ids.btn_run.width = 240
        self.ids.btn_run.add_widget(self.btn_stop)
        self.ids.btn_run.add_widget(
            BoxLayout(size_hint_x=None, width=1)
        )
        self.ids.btn_run.add_widget(self.btn_pause)
        self.proc = Process()
        self.run_event = Clock.schedule_interval(self.do_loop, self.CLOCK)
        self.show_ttbl()
        self.show_configs()

    def do_loop(self, *args):
        self.proc.process()
        if not self.proc.is_proc:
            self.stop()
        if (datetime.now() - self.delta_time).total_seconds() > self.RESUL_TIME:
            self.delta_time = datetime.now()
            self.show_results()
        self.show_status()

    def pause(self, *args):
        Clock.unschedule(self.run_event)

        self.pause_start = datetime.now()

        self.ids.btn_run.remove_widget(self.btn_pause)
        self.ids.btn_run.add_widget   (self.btn_restore)
    
    def restore(self, *args):
        self.run_event = Clock.schedule_interval(self.do_loop, self.CLOCK)

        self.proc.pause_time += datetime.now() - self.pause_start

        self.ids.btn_run.remove_widget(self.btn_restore)
        self.ids.btn_run.add_widget   (self.btn_pause)
    
    def stop(self, *args):
        Clock.unschedule(self.run_event)

        self.ids.btn_run.width = 120
        self.ids.btn_run.clear_widgets()
        self.ids.btn_run.add_widget(self.btn_run)
        
    def show_ttbl(self):
        ttbl_str = ''
        ttbl_lbl = self.side_results.ids.ttbl_lbl
        ttbl = fw.read()['Truth Table']
        lines_number = 0

        for key in ttbl:
            ttbl_str += f'{key}:\n'
            lines_number += 1
            for row_key in ttbl[key]:
                key_space = ''
                for _ in range(3 - len(row_key)):
                    key_space += ' '
                key_space += row_key
                ttbl_str += f'{key_space}: '
                for value in ttbl[key][row_key]:
                    ttbl_str += f'{value} '
                ttbl_str += '\n'
                lines_number += 1

        self.side_results.resize_container()
        ttbl_lbl.text = ttbl_str
        ttbl_lbl.height = self.HEIGHT_COEFNT *\
            ttbl_str.count('\n') * ttbl_lbl.font_size
        self.side_results.resize_container()

    def show_results(self):
        results = self.proc.bests
        scheme_height = self.SCHEME_HEIGHT
        font_size = self.MAX_FONT_SIZE
        container = self.side_results.ids.results_container        
        container.clear_widgets()

        if len(results) > self.RESULT_NO:
            results = results[:-self.RESULT_NO+1]

        for index, result in enumerate(results):
            lbl_height = (
                self.HEIGHT_COEFNT
                * (str(result).count('\n') + 1)
                * int(font_size)
            )
            container.add_widget(Separator10())
            container.add_widget(
                ResultsLbl(
                    text=f'Chromosom #{index+1}',
                    halign='left',
                    height=font_size*self.HEIGHT_COEFNT,
                )
            )
            container.add_widget(
                ResultsLbl(
                    text=str(result),
                    size_hint_y=None,
                    halign='left',
                    height=lbl_height,
                    font_size=font_size,
                )
            )
            scroll_view = ScrollView(do_scroll_x=True, effect_cls='ScrollEffect')
            signals = [f'sgn{number}' for number in range(self.proc.gene_size)]
            scroll_view.add_widget(
                Scheme(
                    height=scheme_height,
                    inputs=signals,
                    outputs=signals,
                    genotype=result.chromosome,
                )
            ) 
            container.add_widget(scroll_view)
            container.add_widget(Separator10())
            
        container.height = ((
            (font_size*self.HEIGHT_COEFNT)
            + scheme_height
            + lbl_height
            + 20)
            * self.RESULT_NO
        ) 

    def show_configs(self):
        configs_str = ''
        configs = self.proc.configs
        configs_lbl = self.side_results.ids.configs_lbl
        
        for key in configs:
            configs_str += f'{key}: {configs[key]["value"]}\n'
        
        self.side_results.resize_container()
        configs_lbl.text = configs_str
        configs_lbl.height = (
            self.HEIGHT_COEFNT
            * len(configs) 
            * (configs_lbl.font_size + 2)
        )
        self.side_results.resize_container()

    def show_plot(self):
        plot.plot([0], self.proc.maxes)
        plot.xlabel('Iterations')
        plot.ylabel('Fitness Function Values')
        plot.grid()
        self.ids.plot.add_widget(Figure(plot.gcf()))

    def refresh_plot(self):
        plot.plot(self.proc.iterations, self.proc.maxes)
        self.ids.plot.clear_widgets()
        self.ids.plot.add_widget(Figure(plot.gcf()))

    def show_status(self):
        self.ids.status_bar.text = f'Progress {self.proc.percent}%'


