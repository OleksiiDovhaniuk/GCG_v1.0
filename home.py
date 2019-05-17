import kivy
kivy.require('1.10.1')
import string


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string('''
<HomeBtnAction@Button>:
    on_press:
        root.manager.transition.direction = 'left'
        root.manager.transition.duration = .30


<HomeScreen>:
    GridLayout:
        cols: 2
        padding: 50
        spacing: 10

        Button:
            id: btSetFunction
            text: "Set Configurations"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = .30
                root.manager.current = 'ConfigurationsScreen'

        Button:
            id: btSetTruthTable
            text: "Set Truth Table"
            on_press:   
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = .30           
                root.manager.current = 'TruthTableScreen'

        Button:
            id: btnExit
            text: "Exit"
            background_color: (.53, .15, .15, 1)
            on_release: app.stop() 

        Button:
            id: btRun
            text: "Run"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = .30
                root.manager.current = 'RunScreen'

 
''')

class HomeBtnAction(Button):
    pass

class HomeScreen(Screen):
    pass
