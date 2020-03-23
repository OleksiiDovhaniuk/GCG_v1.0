import kivy

from kivy.lang                  import Builder
from kivy.uix.screenmanager     import Screen
from kivy.clock                 import Clock

from control.sideConfigurations import Algorithm,\
                                       Inputs,\
                                       Plot
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
        self.side_config_algorithm = Algorithm(minimise=self.minimize_conf)
        self.side_config_inputs    = Inputs   (minimise=self.minimize_conf)
        self.side_config_plot      = Plot     (minimise=self.minimize_conf)

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
        side_cont.add_widget(self.side_config_algorithm)

        self.ids.btn_algorithm.disabled = True
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = False
    
    def show_config_inputs(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.add_widget(self.side_config_inputs)
        
        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = True
        self.ids.btn_plot.disabled      = False
    
    def show_config_plot(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_cont.add_widget(self.side_config_plot)

        self.side_config_algorithm.refresh_widgets()

        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = True

    def minimize_conf(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled    = False
        self.ids.btn_plot.disabled      = False

    def run(self, *args):
        self.ids.btn_run.clear_widgets()
        self.ids.btn_run.width = 240
        self.ids.btn_run.add_widget(self.btn_stop)
        self.ids.btn_run.add_widget(self.btn_pause)

        self.process = Process()
        message      = self.process.message

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
            message = 'Final result: ' + message
            self.stop()

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
        
        
    