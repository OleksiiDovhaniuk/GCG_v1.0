from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty

Builder.load_file('view/lbl.kv')

class Lbl(Label):
    pass

class ResultsLbl(Lbl):
    pass

class TitleLbl(Lbl):
    title = StringProperty('Default')
