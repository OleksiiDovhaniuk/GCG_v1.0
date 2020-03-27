import kivy

from kivy.lang                  import Builder
from kivy.uix.screenmanager     import Screen
from kivy.clock                 import Clock
from kivy.uix.boxlayout         import BoxLayout

from control.sideConfigurations import Algorithm,\
                                       Inputs,\
                                       Plot,\
                                       Results
from control.dropDownMenu       import DropDownMenu
from control.lbl                import Lbl
from control.btn                import Btn

from process                    import Process
from design                     import Design
from functools                  import partial
from datetime                   import datetime

kivy   .require  ('1.10.1')
Builder.load_file('view/main.kv')

class Main(Screen):
    theme = Design().default_theme

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.side_config_algorithm = Algorithm(title='Algorithm Configurations',
                                               minimise=self.minimize_conf)
        self.side_config_inputs    = Inputs   (title='Inputs Configurations',
                                               minimise=self.minimize_conf)
        self.side_config_plot      = Plot     (title='Plot Configurations',
                                               minimise=self.minimize_conf)
        self.side_results          = Results  (title='Results',
                                               minimise=self.minimize_conf)

        self.btn_run     = Btn(text ='Run')
        self.btn_pause   = Btn(text ='Pause')
        self.btn_restore = Btn(text ='Restore')
        self.btn_stop    = Btn(text ='Stop')

        self.btn_run    .bind(on_release=self.run)
        self.btn_pause  .bind(on_release=self.pause)
        self.btn_restore.bind(on_release=self.restore)
        self.btn_stop   .bind(on_release=self.stop)

        self.pause_start = None

    def show_config_algorithm(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 360
        side_cont.add_widget(self.side_config_algorithm)

        self.ids.btn_algorithm.disabled = True
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = False
        self.ids.btn_results.disabled   = False
    
    def show_config_inputs(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 360
        side_cont.add_widget(self.side_config_inputs)
        
        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = True
        self.ids.btn_plot.disabled      = False
        self.ids.btn_results.disabled   = False
    
    def show_config_plot(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 360
        side_cont.add_widget(self.side_config_plot)

        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = True
        self.ids.btn_results.disabled   = False

    def show_side_results(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 360
        side_cont.add_widget(self.side_results)

        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = False
        self.ids.btn_results.disabled   = True

    def minimize_conf(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.width = 0
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = False
        self.ids.btn_results.disabled   = False

    def run(self, *args):
        self.ids.btn_run.clear_widgets()
        self.ids.btn_run.width = 240
        self.ids.btn_run.add_widget(self.btn_stop)
        self.ids.btn_run.add_widget(BoxLayout(size_hint_x=None,
                                              width=1))
        self.ids.btn_run.add_widget(self.btn_pause)

        self.process = Process()
        message      = self.process.message
        self.show_ttbl()
        self.show_configs()

        self.ids.status_bar.text  = message
        self.ids.status_bar.width = (len(message) + 1) * 10
        self.run_event = Clock.schedule_interval(self.do_loop,  1)

    def do_loop(self, *args):
        process = self.process
        process.do_loop()
        message = process.message
        configs = process.configurations

        if ((configs['iterations limit']['active'] and
                process.iterations >= configs['iterations limit']['value']) or
            (configs['process time']['active'] and
                process.int_time >= configs['process time']['value'])):
            self.show_genotypes()
            message = 'Final result: ' + message
            self.stop()
        elif process.have_result:
            self.show_genotypes()

        self.ids.status_bar.text  = message
        self.ids.status_bar.width = (len(message) + 1) * 10

    def pause(self, *args):
        Clock.unschedule(self.run_event)

        self.pause_start = datetime.now()

        self.ids.btn_run.remove_widget(self.btn_pause)
        self.ids.btn_run.add_widget   (self.btn_restore)
    
    def restore(self, *args):
        self.run_event = Clock.schedule_interval(self.do_loop,  1)

        self.process.pause_time += datetime.now() - self.pause_start

        self.ids.btn_run.remove_widget(self.btn_restore)
        self.ids.btn_run.add_widget   (self.btn_pause)
    
    def stop(self, *args):
        Clock.unschedule(self.run_event)

        self.ids.btn_run.width = 120
        self.ids.btn_run.clear_widgets()
        self.ids.btn_run.add_widget(self.btn_run)
        
    def show_ttbl(self):
        ttbl_str = ''
        ttbl     = self.process.truth_table
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
                    if value == None: ttbl_str += 'X '
                    else: ttbl_str += f'{str(value)} '
                ttbl_str += '\n'
                lines_number += 1

        self.side_results.lines_number += lines_number - 1
        self.side_results.resize_container()
        self.side_results.widgets['Truth Table'][1].text   = ttbl_str
        self.side_results.widgets['Truth Table'][1].height = lines_number * 24

    def show_schemes(self):
        pass

    def show_genotypes(self):
        process = self.process
        if process.have_result: genotypes = process.proper_results
        else: genotypes = process.best_results.iloc[:5, :]
        genotypes_str  = ''

        for index, value in enumerate(genotypes['value'].tolist()):
            chromosome_str = ['' for _ in range(len(genotypes.iloc[0, 0][0]))]
            genotypes_str += f'Chromosom #{index+1}:\n' 

            for gene in genotypes.iloc[index, 0]:
                for jndex, alet in enumerate(gene):
                    chromosome_str[jndex] += f'{alet}'

            for gene_str in chromosome_str:
                genotypes_str += f'{gene_str}\n'

            value_round = round(value, 6)
            str_time    = str(process.best_results.iloc[index, 2])[7:18] 
            genotypes_str += f'Fitness Function value {value_round} \n'
            genotypes_str += f'Search Time {str_time}\n\n'

        self.side_results.widgets['Genotypes'][1].text   = genotypes_str
        self.side_results.widgets['Genotypes'][1].height = 1000

    def show_configs(self):
        configs_str = ''
        configs = self.process.configurations
        lines_number = len(configs)
        for key in configs:
            configs_str += f'{key}: '
            configs_str += f'{configs[key]["value"]}\n'
        
        self.side_results.resize_container()
        self.side_results.widgets['Configurations'][1].text = configs_str
        self.side_results.widgets['Configurations'][1].height = 300