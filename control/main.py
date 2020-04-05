import kivy

from kivy.lang                  import Builder
from kivy.uix.screenmanager     import Screen
from kivy.clock                 import Clock
from kivy.uix.boxlayout         import BoxLayout
from kivy.uix.scrollview        import ScrollView

from control.sideConfigurations import Algorithm,\
                                       Input    ,\
                                       Plot     ,\
                                       Results
from control.dropDownMenu       import DropDownMenu
from control.lbl                import Lbl,\
                                       ResultsLbl
from control.btn                import Btn
from control.scheme             import Scheme
from control.layout             import Separator10

from process                    import Process
from design                     import Design
from functools                  import partial
from datetime                   import datetime

kivy   .require  ('1.10.1')
Builder.load_file('view/main.kv')

class Main(Screen):
    theme = Design().default_theme
    SCHEME_HEIGHT = 150
    MAX_FONT_SIZE = 16
    HEIGHT_COEFNT = 1.5

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.side_config_algorithm = Algorithm(title='Algorithm Configurations',
                                               minimise=self.minimize_conf)
        self.side_config_input     = Input    (title='Input Configurations',
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
        side_cont.add_widget(self.side_config_input)
        
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
            self.show_results()
            message = 'Final result: ' + message
            self.stop()
        elif process.have_result:
            self.show_results()

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
        ttbl_lbl = self.side_results.ids.ttbl_lbl
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
                ttbl_str  += f'{key_space}: '
                for value in ttbl[key][row_key]:
                    if value == None: ttbl_str += 'X '
                    else: ttbl_str += f'{str(value)} '
                ttbl_str += '\n'
                lines_number += 1

        self.side_results.resize_container()
        ttbl_lbl.text   = ttbl_str
        ttbl_lbl.height = self.HEIGHT_COEFNT *\
            ttbl_str.count('\n') * ttbl_lbl.font_size
        self.side_results.resize_container()

    def show_results(self):
        process         = self.process
        scheme_height   = self.SCHEME_HEIGHT
        genotype_str = ''

        if process.have_result: genotypes = process.proper_results
        else: genotypes = process.best_results.iloc[:5, :]

        # for genotype in genotypes['chromosome'].tolist():
        #     for gene in genotype:
        #         NaN_number = gene.count([0, 0])
        #         if NaN_number == len(gene):
        #             genotype.remove(gene)
        #         NaN_number = 0

        values_list = genotypes['value'].tolist()
        container   = self.side_results.ids.results_container        
        container.clear_widgets()

        for index, value in enumerate(values_list):
            chromosome_str = ['' for _ in range(len(genotypes.iloc[0, 0][0]))]
            text_top       = f'Chromosom #{index+1}:' 

            for gene in genotypes.iloc[index, 0]:
                for jndex, alet in enumerate(gene):
                    chromosome_str[jndex] += f'{alet}'

            for gene_str in chromosome_str:
                genotype_str += f'{gene_str}\n'
            
            font_size = self.HEIGHT_COEFNT\
                * self.side_results.width / len(chromosome_str[0])
            if font_size > self.MAX_FONT_SIZE:
                font_size = self.MAX_FONT_SIZE

            value_round  = round(value, 6)
            str_time     = str(process.best_results.iloc[index, 2])[7:18] 
            text_bottom  = f'Fitness Function value {value_round} \n'
            text_bottom += f'Search Time {str_time}\n'
            text_bottom += f'Scheme:'

            lbl_height    = self.HEIGHT_COEFNT\
                * genotype_str.count('\n') * int(font_size)

            container.add_widget(Separator10())
            container.add_widget(ResultsLbl(text=text_top,
                                            halign='left',
                                            height=21))
            container.add_widget(ResultsLbl(text=genotype_str,
                                            size_hint_y=None,
                                            height=lbl_height,
                                            font_size=font_size))
            container.add_widget(ResultsLbl(text=text_bottom,
                                            halign='left',
                                            height=84))

            scroll_view = ScrollView(do_scroll_x=True, 
                                     effect_cls='ScrollEffect')
            scroll_view.add_widget(Scheme(height=scheme_height,
                                          genotype=genotypes.iloc[index, 0])) 
            container.add_widget(scroll_view)
            container.add_widget(Separator10())
            
            genotype_str = ''

        container.height = (125 + scheme_height + lbl_height ) * len(values_list)

    def show_configs(self):
        configs_str = ''
        configs     = self.process.configurations
        configs_lbl = self.side_results.ids.configs_lbl
        lines_number = len(configs)
        for key in configs:
            configs_str += f'{key}: '
            configs_str += f'{configs[key]["value"]}\n'
        
        self.side_results.resize_container()
        configs_lbl.text   = configs_str
        configs_lbl.height = self.HEIGHT_COEFNT *\
            configs_str.count('\n') * (configs_lbl.font_size + 2)
        self.side_results.resize_container()