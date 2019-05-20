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
    font_size: 14
    markup: True
<UbuntuActBtn@ActionButton>:
    font_name: 'res/fonts/ubuntu-font-family-0.80/Ubuntu-M.ttf'
    font_size: 14
    markup: True

<HomeScreen>:
    GridLayout:
        cols: 1
        rows: 3
        ActionBar:
            size: (100, 40)
            size_hint: (1, None)
            pos_hint: {'top':1}
            background_image: 'res/images/bg_normal.png'
            background_color: hex('#161b1e')
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'GCG v1.0'
                    with_previous: False
                ActionGroup:
                    text: 'File' 
                    mode: 'spinner'
                    size_hint: (0.3, 1)
                    
                    UbuntuActBtn:
                        id: btSetFunction
                        text: "Configurations"
                        background_color: hex('#b7e3ff')
                        on_release:
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30
                            root.manager.current = 'ConfigurationsScreen'
                    UbuntuActBtn:
                        id: btSetTruthTable
                        text: "Set Truth Table"
                        background_color: hex('#b7e3ff')
                        on_release:   
                            root.manager.transition.direction = 'left'
                            root.manager.transition.duration = .30           
                            root.manager.current = 'TruthTableScreen'
                    UbuntuActBtn:
                        id: btnExit
                        text: "Exit"
                        background_color: hex('#b7e3ff')
                        color: hex('#d14d70')
                        on_release: app.stop() 
                UbuntuActBtn:
                    id: btRun
                    text: "Run"
                    pos_hint: {'center':1}
                    color: hex('#74f0f7')
                    size_hint: (0.3, 1)
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
