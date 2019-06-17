import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout

# own classes imports
import process

Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
#:import utils kivy.utils
<HomeBtnAction@Button>:
    on_press:
        root.manager.transition.direction = 'left'
        root.manager.transition.duration = .30
<UbuntuLbl@Label>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    font_size: 16
    markup: True
    color: (0,0,0,1)
<UbuntuActBtn@ActionButton>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_image: 'res/images/bg_normal.png'
    background_color: hex('#707070')
    font_size: 18
    markup: True
    color: (0,0,0,1)
<UbuntuBtn@Button>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_normal: 'res/images/bg_normal.png'
    background_color: hex('#edf9ff')
    size_hint: (None, None)
    size: (150, 35)
    font_size: 16
    markup: True
    color: (0,0,0,1)
<ClearBtn@BoxLayout>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_normal: 'res/images/bg_clear.png'
    background_down: 'res/images/bg_clear_on_press.png'
    size_hint: (None, None)
    size: (150, 35)
    font_size: 16
    markup: True
    color: (0,0,0,1)
<UbuntuTxtIn@TextInput>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_image: 'res/images/bg_normal.png'
    background_disabled_down: hex('#707070')
    font_size: 16
    markup: True
    color: (0,0,0,1)
<HomeScreen>:
    on_enter: 
        dropdown_file.dismiss(self)
        dropdown_action.dismiss(self)
        dropdown_info.dismiss(self)
    GridLayout:
        cols: 1
        rows: 3
        spasing: 5
        BoxLayout:
            orientation: 'horizontal'
            size: (30, 30)
            size_hint: (1, None)
            canvas.before:
                Color:
                    rgb: utils.get_color_from_hex('#dae3e8')
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
                        text: 'Configurations'
                        on_release: root.manage_file(self.text)
                    UbuntuBtn:
                        text: 'Set truth table'
                        on_release: root.manage_file(self.text)
                    UbuntuBtn:
                        text: 'Save job'
                        on_release:
                    UbuntuBtn:
                        text: 'Exit'
                        on_release: root.manage_file(self.text)
            UbuntuBtn:
                id: btn_action
                text: 'Action'
                on_release: dropdown_action.open(self)
                DropDown:
                    id: dropdown_action
                    UbuntuBtn:
                        text: 'New start'
                        on_release: root.manage_action()
            UbuntuBtn:
                id: btn_info
                text: 'Info'
                on_release: dropdown_info.open(self)
                DropDown:
                    id: dropdown_info
                    UbuntuBtn:
                        text: 'Tutorial'
                        on_release:
                    UbuntuBtn:
                        text: 'About GGC'
                        on_release:

            UbuntuLbl:
                size: (200, 30)
                size_hint: (None, 1)
        BoxLayout:
            orientation: 'vertical'
            UbuntuLbl:
                id: lblInfo
                text: "INFO"
        
''')

class UbuntuBtn(Button):
    pass

class HomeScreen(Screen):
    def manage_file(self, file_value):
        self.ids.dropdown_file.dismiss()
        if file_value == 'Exit':
            self.stop()
        else:
            self.manager.transition.direction = 'left'
            self.manager.transition.duration = .30
            if file_value == 'Configurations':
                self.manager.current = 'ConfigurationsScreen'
            else: 
                self.manager.current = 'TruthTableScreen'

    def manage_action(self):
        self.ids.dropdown_action.dismiss()
        process.new_start()
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .30           
        self.manager.current = 'ActionScreen'


    
