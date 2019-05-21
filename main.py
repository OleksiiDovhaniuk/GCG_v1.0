from kivy.app import App
from kivy.core.window import Window
from setUp import SetUp

set_up = SetUp()

class mainApp(App):
    set_up.set_up()

    def build(self):
        Window.toggle_fullscreen()
        Window.fullscreen = False
        # Window.fullscreen = True
        # self.icon = 'ICOs/Graphicloads-Flat-Finance-Global.ico'
        self.title = 'GGC v1.0'
        Window.clearcolor = (.12, .14, .15, 1)
        return set_up.screen_manager


sample_app = mainApp()
sample_app.run()

if __name__ == '__main__':
    import doctest
    doctest.testmod()