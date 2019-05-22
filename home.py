import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
<HomeBtnAction@Button>:
    on_press:
        root.manager.transition.direction = 'left'
        root.manager.transition.duration = .30
<UbuntuLbl@Label>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    font_size: 18
    markup: True
    color: (0,0,0,1)
<UbuntuActBtn@ActionButton>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_image: 'res/images/bg_normal.png'
    background_color: hex('#e3eaea')
    font_size: 18
    markup: True
    color: (0,0,0,1)

<UbuntuBtn@Button>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_image: 'res/images/bg_normal.png'
    background_color: hex('#e3eaea')
    font_size: 18
    markup: True
    color: (0,0,0,1)

<UbuntuTxtIn@TextInput>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    background_image: 'res/images/bg_normal.png'
    background_disabled_down: hex('#e3eaea')
    font_size: 18
    markup: True
    color: (0,0,0,1)

<HomeScreen>:
    GridLayout:
        cols: 1
        rows: 3
        ActionBar:
            size: (100, 40)
            size_hint: (1, None)
            pos_hint: {'top':1}
            background_image: 'res/images/bg_normal.png'
            background_color: hex('#e3eaea')
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'GGC v1.0'
                    with_previous: False
                    font_size: 18
                    color: (0,0,0,1)
                ActionGroup:
                    text: 'File' 
                    mode: 'spinner'
                   
                    size_hint: (.3, 1)
                    color: (0,0,0,1)
                    UbuntuActBtn:
                        id: btSetFunction
                        text: "Configurations"
                        on_release:
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30
                            root.manager.current = 'ConfigurationsScreen'
                        
                    UbuntuActBtn:
                        id: btSetTruthTable
                        text: "Set Truth Table"
                        on_release:   
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30           
                            root.manager.current = 'TruthTableScreen'
                    UbuntuActBtn:
                        id: btnExit
                        text: "Exit"
                        color: hex('#0e7c7c')
                        on_release: app.stop() 
                UbuntuActBtn:
                    id: btRun
                    text: "Run"
                    pos_hint: {'center':1}
                    color: hex('#0e7c7c')
                    size_hint: (.3, 1)
                    on_release:
                        root.manager.transition.direction = 'left'
                        root.manager.transition.duration = .30
                        root.manager.current = 'RunScreen'
                
        BoxLayout:
            orientation: 'vertical'
            UbuntuLbl:
                id: lblInfo
                text: "INFO"
 
''')

class HomeBtnAction(Button):
    pass

class HomeScreen(Screen):
    pass
