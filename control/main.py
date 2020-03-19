import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from control.sideConfigurations import Algorithm, Inputs, Plot
from control.btn import MenuBarBtn


kivy.require('1.10.1')
Builder.load_file('view/main.kv')

class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

    def show_config_algorithm(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_config = Algorithm(minimise=self.minimize_conf)
        side_cont.add_widget(side_config)
        self.ids.btn_algorithm.disabled = True
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
    
    def show_config_inputs(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_config = Inputs(minimise=self.minimize_conf)
        side_cont.add_widget(side_config)
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = True
        self.ids.btn_plot.disabled = False
    
    def show_config_plot(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        side_config = Plot(minimise=self.minimize_conf)
        side_cont.add_widget(side_config)
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = True

    def minimize_conf(self, *args):
        side_cont = self.ids.side_conf_container
        side_cont.clear_widgets()
        self.ids.btn_algorithm.disabled = False
        self.ids.btn_inputs.disabled = False
        self.ids.btn_plot.disabled = False
