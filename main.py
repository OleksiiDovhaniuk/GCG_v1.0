from kivy.app import App
from kivy.core.window import Window
from setUp import SetUp
import pyqtgraph.examples


set_up = SetUp()


class mainApp(App):
    set_up.set_up()

    def build(self):
        Window.size = 600, 400
        # Window.fullscreen = True
        # self.icon = 'ICOs/Graphicloads-Flat-Finance-Global.ico'
        self.title = 'GCG v1.0'
        Window.clearcolor = (.12, .14, .15, 1)
        return set_up.screen_manager


sample_app = mainApp()
sample_app.run()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    pyqtgraph.examples.run()