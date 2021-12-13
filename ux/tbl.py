"""
:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      28.03.2021

"""
import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

from ux.lbl import Lbl
from ux.layout import Line1Dark, LightDefault
from ux.btn import Btn

kivy   .require('1.10.1')
Builder.load_file('ui/tbl.kv')


class TruthTbl(BoxLayout):
    _stypes = ('input', 'output')
    # Table.
    tbl = {stype: [] for stype in _stypes}
    # Widgets.
    wgt = {stype: [] for stype in _stypes}
    base = 2
    cols = 0
    rows = 0

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.size_hint_y = None
        wgt = self.wgt

        for stype in self._stypes:
            layout = BoxLayout(orientation='vertical', size_hint_y=None)
            self.add_widget(layout)
            wgt[stype] = [BoxLayout(size_hint_y=None, height=32),
                          LightDefault(size_hint_y=None)]

            layout.add_widget(wgt[stype][0])
            layout.add_widget(Line1Dark())
            layout.add_widget(wgt[stype][1])
            layout.bind(minimum_height=layout.setter('height'))
            wgt[stype][1].bind(minimum_height=wgt[stype][1].setter('height'))

        self.bind(minimum_height=self.setter('height'))

    def edit_signal(self, stype, index, new_title):
        self.tbl[stype][index]['Title'].text = new_title

    def add_signal(self, titles):
        tbl = self.tbl
        base = self.base
        cols = self.cols = self.cols + 1
        rows = base ** cols

        for title, stype in zip(titles, self._stypes):
            # Add a new column.
            title_lbl = TitleCell(text=title)
            self.wgt[stype][0].add_widget(title_lbl)

            box = BoxLayout(orientation='vertical',
                            size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))

            self.wgt[stype][1].add_widget(box)

            if stype == 'input':
                cells = [Lbl(
                    text=str(int(i // (rows/base))),
                    size_hint_y=None,
                    height=30,
                    halign='center'
                ) for i in range(rows)]
            else:
                cells = [Btn(text='0', size_hint=(1, None), height=32)
                         for _ in range(rows)]
                for cell in cells:
                    cell.bind(on_press=self._switch)

            for cell in cells:
                box.add_widget(cell)

            new_col = {
                'Title': title_lbl,
                'Column': box,
                'Cells': cells}
            tbl[stype].append(new_col)

            # Update previouse signals
            for i in range(cols-1):
                l = len(self.tbl[stype][i]['Cells'])  # Cells length
                for j in range(l, rows):
                    for stype in self._stypes:
                        if stype == 'input':
                            cell = Lbl(
                                text=self.tbl[stype][i]['Cells'][j-l].text,
                                size_hint_y=None,
                                height=30,
                                halign='center')
                        else:
                            cell = Btn(
                                size_hint=(1, None),
                                height=32,
                                text='0')
                            cell.bind(on_press=self._switch)
                        self.tbl[stype][i]['Column'].add_widget(cell)
                        self.tbl[stype][i]['Cells'].append(cell)

    def delete_signal(self, index):
        for i in range(2):
            column = self.tbl[i].pop(index)
            self.wgt[i][0].remove_widget(column['title'])
            self.wgt[i][1].remove_widget(column['layout'])

        self.cols -= 1
        if self.cols:
            self.rows = self.base ^ self.cols
        else:
            self.rows = 0

    def _switch(self, cell):
        cell.text = str((int(cell.text) + 1) % self.base)


class TitleCell(Lbl):
    pass
