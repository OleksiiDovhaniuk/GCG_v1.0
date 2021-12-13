from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window

from ux.main import Main

# deny to resize windows
<<<<<<< HEAD
# Config.set('graphics', 'borderless', True)
# Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', 2000)
Config.set('graphics', 'height', 1000)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 300)
Config.set('graphics', 'top',  200)
Config.set('graphics', 'fullscreen',  False)
Config.set('graphics', 'borderless', True)
=======
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')
>>>>>>> parent of 395bcd5 (Restart workflow)

Config.set('graphics', 'resizable', True)
Config.set('kivy', 'keyboard_mode', 'system')
# save configurations
Config.write()


class mainApp(App):
    def build(self):
        Window.toggle_fullscreen()
        Window.fullscreen = False
        # Window.borderless = True
        Window.minimum_width, Window.minimum_height = Window.size
        self.icon = 'res/icon/logo.png'
        self.title = 'QubitLab'
        Window.clearcolor = (1, 1, 1, 1)

        return Main()


qubit_app = mainApp()
qubit_app.run()
