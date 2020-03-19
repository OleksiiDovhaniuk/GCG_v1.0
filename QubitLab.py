from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from prep import Prep

# deny to resize windows
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'keyboard_mode', 'system')
# save configurations
Config.write()

prep = Prep()

class mainApp(App):
    prep.prep()

    def build(self):
        Window.toggle_fullscreen()
        Window.fullscreen = False
        self.icon = 'res/icons/logo.png'
        self.title = 'QubitLab'
        Window.clearcolor = (1, 1, 1, 1)
        return prep.screen_manager

sample_app = mainApp()
sample_app.run()

if __name__ == '__main__':
    import doctest
    doctest.testmod()