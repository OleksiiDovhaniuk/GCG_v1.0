import kivy
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
    ObjectProperty,
    StringProperty,
)

from ux.layout import (
    ViewLayout,
)
from ux.lbl import Lbl
from ux.btn import Btn

kivy   .require('1.10.1')
Builder.load_file('ui/basisView.kv')
    

class BasisView(ViewLayout):
    _scroll_view = ScrollView(
            size_hint_y=None,
            effect_cls='ScrollEffect',
        )
    _table = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
    )
    _table.bind(minimum_height=_table.setter('height'))

    _scroll_view.add_widget(_table)

    _data = [
        {
            'Designation': 'CNOT2B',
            'Base': 'bit',
            'Delay': '2.0',
            'Qcost': '2',
            'Total Logical Cost': 'a+3b+3y',
            'Parity': 'Yes',
        },
        {
            'Designation': 'FRG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+3b+y',
            'Parity': 'Yes',
        },
        {
            'Designation': 'TFG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+b+4y',
            'Parity': 'No',
        },
        {
            'Designation': 'TFG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+b+4y',
            'Parity': 'No',
        },
        {
            'Designation': 'TFG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+b+4y',
            'Parity': 'No',
        },
        {
            'Designation': 'TFG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+b+4y',
            'Parity': 'No',
        },
        {
            'Designation': 'TFG3B',
            'Base': 'bit',
            'Delay': '5.0',
            'Qcost': '5',
            'Total Logical Cost': '2a+b+4y',
            'Parity': 'No',
        },
    ]

    def __init__(self):
        ViewLayout.__init__(self, 'Basis')
        self.spacing = 0
        self._del_popup = DelPopup()

        titles = self._titles = TitleRow()
        titles.ids.checkbox.bind(on_press=self.check_all) 
        self.add_widget(titles)
        
        self._rows = [DataRow(
                desig=row['Designation'], 
                base=row['Base'], 
                delay=row['Delay'],
                qcost=row['Qcost'],
                tlc=row['Total Logical Cost'],
                parity=row['Parity'],
            ) for row in self._data]
        for row in self._rows:
            self._table.add_widget(row)
            row.ids.checkbox.bind(on_press=self.check_one)
            row.ids.del_btn.bind(on_release=self.open_del_popup)

        
        self._scroll_view.bind(size=self.update)

        self.add_widget(self._scroll_view)
        self.add_widget(BoxLayout())

        add_btn = AddRowBtn() 
        self.add_widget(BoxLayout(size_hint_y=None, height=sp(12)))
        self.add_widget(add_btn)

    def check_all(self, checkbox):
        value = checkbox.active

        for row in self._rows:
            row.ids.checkbox.active = value

    def check_one(self, checkbox):
        value = checkbox.active
        title_checkbox = self._titles.ids.checkbox

        if value:
            if all([row.ids.checkbox.active for row in self._rows]):
                title_checkbox.active = value
        else:
            title_checkbox.active = value

    def update(self, *args):
        self._scroll_view.height = self.height - sp(22)

    def open_del_popup(self, btn):
        popup = self._del_popup
        del_btn = popup.ids.del_btn

        popup.desig = btn.desig
        del_btn.table = btn.table
        del_btn.row = btn.row

        popup.open()
        popup.ids.txt_input.focus = True


    def get_data(self):
        pass

class DataRow(BoxLayout):
    desig = StringProperty()
    base = StringProperty()
    delay = StringProperty()
    qcost = StringProperty()
    tlc = StringProperty()
    parity = StringProperty()
    
    def __init__(self, desig, base, delay, qcost, tlc, parity):
        BoxLayout.__init__(self)
        
        self.desig = desig
        self.base = base
        self.delay = delay
        self.qcost = qcost
        self.tlc = tlc
        self.parity = parity

class DelPopup(Popup):
    desig = StringProperty()
    table = ObjectProperty()
    row = ObjectProperty()

    def __init__(self):
        Popup.__init__(self)

        # self.table = self.parent._table

        self.ids.txt_input.bind(text=self.check_del)
        self.ids.del_btn.bind(on_release=self.dismiss)

    def check_del(self, txt_input,*args):
        if txt_input.text in ('delete', 'Delete', 'DELETE'):
            self.ids.del_btn.disabled = False
        else:
            self.ids.del_btn.disabled = True

    def dismiss(self, *args):
        self.ids.txt_input.text = ''

        # self.desig = ''
        # self.table = ObjectProperty()
        # self.row = ObjectProperty()

        Popup.dismiss(self)


class TableTitle(Btn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._filter = FilterDropdown(self)

    def on_release(self):
        self._filter.open(self)
        self.disabled = True

        return super().on_release()

class TableLbl(Lbl):
    pass

class DataLbl(TableLbl):
    pass

class TitleRow(BoxLayout):
    pass

class EditRowBtn(Btn):
    pass

class DelRowBtn(Btn):
    pass

class AddRowBtn(Btn):
    pass

class PopupDelBtn(Btn):
    table = ObjectProperty()
    row = ObjectProperty()

    def on_release(self):
        try: 
            self.table.remove_widget(self.row)
        except ValueError as e:
            print(f'ValueException: {e} (Tried to remove {self.row} from {self.table})')


class SeparatorH1sp(BoxLayout):
    pass

class FilterDropdown(DropDown):
    def __init__(self, btn, **kwargs):
        super(FilterDropdown, self).__init__(**kwargs)
        self._parent_btn = btn

    def on_dismiss(self):
        self._parent_btn.disabled = False
        return super().on_dismiss()

class SortBtn(Btn):
    sort_dir = StringProperty('AZ')
            
                