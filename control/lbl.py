from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy import utils

Builder.load_file('view/lbl.kv')

class Lbl(Label):
    pass

class InfoConfigLbl(Lbl):
    STATUS = {
        'Default': utils.get_color_from_hex('#A1A1A1'), 
        'Help': utils.get_color_from_hex('#32A4CE'),
        'Error': utils.get_color_from_hex('#EC512F'),
    }
    status = StringProperty('Default')

    def change_status_to(self, status):
        """ Change status of the Label and all properties related to it.

        Args: status ("Default", "Help", "Error")

        """
        if status in self.STATUS:
            self.status = status
            self.color = self.STATUS[status]

class ResultsLbl(Lbl):
    pass

class TitleLbl(Lbl):
    title = StringProperty('Default')
