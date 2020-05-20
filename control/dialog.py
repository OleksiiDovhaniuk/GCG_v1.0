from functools import partial

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from pandas import DataFrame

from control.cell import AddCell, Cell, EmptyCell, IndexCell, TitleCell
from control.flChsr import FlChsrIconLayout, FlChsrListLayout
from control.layout import TTblRow
from design import Design
from file_work import STORAGE_PATH


Builder.load_file('view/dialog.kv')

class Dialog(FloatLayout):
    theme = Design().default_theme
    cancel = ObjectProperty(None)
    path = StringProperty(STORAGE_PATH)

class Load(Dialog):
    load = ObjectProperty(None)

class Save(Dialog):
    save = ObjectProperty(None)
    data = ObjectProperty(None)

class TruthTable(Dialog):
    get_ttbl = ObjectProperty(None)
    reset = ObjectProperty(None)
    truth_table = ObjectProperty(None)
    cells = {'inputs': [], 'outputs': []}
    signals = []

    def __init__(self, truth_table, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.truth_table = truth_table
        self.signals = []

        for table in ['inputs', 'outputs']:
            self.create_table(table)
        self.resize()
        
    def create_table(self, table):
        values = self.truth_table[table].replace([None], 'X')
        tbl = self.ids[f'{table}_tbl']
        row = TTblRow() 
        row.add_widget(EmptyCell(text=''))
        key_widgets = [row, 'indices']

        for index, key in enumerate(values):
            cell = TitleCell(
                text=key, 
                cell_type=table,
                index=index+2,
                remove_column=self.remove_column,
                valid_to_apply=self.valid_to_apply,
                is_equal_signal=self.is_equal_signal,
                erase_signal=self.erase_signal,
                write_column=self.write_column
            )
            row.add_widget(cell)
            key_widgets.append(cell)

            self.signals.append(key.replace(' ', ''))

        add_cell_column = AddCell(cell_type=table)
        row.add_widget(add_cell_column)
        key_widgets.append(add_cell_column)
        tbl.add_widget(row)

        widgets = []
        for index in range(values.shape[0]):
            row = TTblRow() 
            index_cell = IndexCell(index=index)
            row.add_widget(index_cell)
            row_widgets = [row, index_cell]
        
            for key in values:
                value = values[key][index]
                cell = Cell(text=str(value), cell_type=table)
                row.add_widget(cell)
                row_widgets.append(cell)

            tbl.add_widget(row)
            widgets.append(row_widgets)

        row = TTblRow()
        add_cell = AddCell(cell_type=table)
        row.add_widget(add_cell)
        tbl.add_widget(row)
        row_widgets = [None for _ in range(len(key_widgets))]
        row_widgets[0] = row
        row_widgets[1] = add_cell
        widgets.append(row_widgets)

        align_lt = TTblRow(size_hint_y=1)
        tbl.add_widget(align_lt)
        row_widgets = [None for _ in range(len(key_widgets))]
        row_widgets[0] = align_lt
        widgets.append(row_widgets)

        self.cells[table] = DataFrame(data=widgets,
                                columns=key_widgets)

        for index, cell in enumerate(self.cells[table]['indices'][:-2]):
            cell.bind(on_release=partial(self.remove_row, cell))

        add_cell.bind(on_release=partial(self.add_row, add_cell))
        add_cell_column.bind(on_release=partial(self.add_column, add_cell_column))
        
    def remove_row(self, instance, *args):
        index = instance.index

        for table in ['inputs', 'outputs']:
            tbl = self.ids[f'{table}_tbl']
            cells = self.cells[table] 
            index_cells = cells.iloc[index+1:-2, 1].values.tolist()

            tbl.remove_widget(cells.iloc[index, 0])
            cells = cells.drop([index])
            
            cells.iloc[-2, 1].index = len(index_cells) + 1
            for jndex, index_cell in enumerate(index_cells):
                kndex = index + jndex 

                index_cell.index = kndex
                index_cell.title = str(kndex + 1)
                index_cell.text = str(kndex + 1)

            self.cells[table] = cells.reset_index(drop=True)

        self.resize()

    def add_row(self, *args):
        for table in ['inputs', 'outputs']:
            tbl = self.ids[f'{table}_tbl']
            cells = self.cells[table] 
            index = len(cells.index) - 2
            row = cells.iloc[-2, 0]

            row.clear_widgets()

            index_cell = IndexCell(index=index,
                                   on_release=self.remove_row)
            row.add_widget(index_cell)
            widgets = [
                [row, index_cell],
                [None for _ in cells.columns],
                [None for _ in cells.columns]
            ]

            for _ in cells.columns[2:-1]:
                cell = Cell(cell_type=table)
                widgets[0].append(cell)
                row.add_widget(cell)
            
            add_cell = cells.iloc[-2, 1]
            last_row = cells.iloc[-1, 0]
            add_cell.index = index + 1
            last_row.size_hint_y = None
            last_row.height = add_cell.height
            last_row.add_widget(add_cell)
            widgets[1][0] = last_row
            widgets[1][1] = add_cell

            new_row = TTblRow(size_hint_y=1)
            widgets[2][0] = new_row
            tbl.add_widget(new_row)

            cells = cells.drop([index, index+1])
            new_data_frame = DataFrame(data=widgets, columns=cells.columns)
            cells = cells.append(new_data_frame)
            self.cells[table] = cells.reset_index(drop=True)

        self.resize()

    def remove_column(self, instance, *args):
        table = instance.cell_type
        index = instance.index
        cells = self.cells[table] 
        column_size = len(cells.index) - 2
        columns = cells.columns

        if instance.reserved_title in self.signals:
            self.signals.remove(instance.reserved_title)

        columns[0].remove_widget(columns[index])
        for cell in columns[1+index: -1]:
            cell.index -= 1
        for jndex, row in enumerate(cells.iloc[:column_size, 0].values):
            row.remove_widget(cells.iloc[jndex, index])


        self.cells[table] = self.cells[table].drop(columns=[columns[index]])
        self.resize()

    def add_column(self, instance, *args):
        table = instance.cell_type
        cells = self.cells[table] 
        columns = cells.columns
        add_index = len(columns) - 1
        column_size = len(cells.index) - 2
        add_cell = columns[add_index]
        
        columns[0].remove_widget(add_cell)
        key_cell = TitleCell(
            index=add_index,
            cell_type=table,
            remove_column=self.remove_column,
            valid_to_apply=self.valid_to_apply,
            is_equal_signal=self.is_equal_signal,
            erase_signal=self.erase_signal,
            write_column=self.write_column
        )
        columns[0].add_widget(key_cell)
        key_cell.focus = True
        columns[0].add_widget(add_cell)

        column_widgets = []
        for index in range(column_size):
            cell = Cell(text='0', cell_type=table)
            cells.iloc[index, 0].add_widget(cell)
            column_widgets.append(cell)
        for _ in range(2):
            column_widgets.append(None)

        self.cells[table].insert(add_index, key_cell, column_widgets, False)
        self.resize()
        
    def valid_to_apply(self, *args):
        ins_size = len(self.cells['inputs'] .columns)
        outs_size = len(self.cells['outputs'].columns)
        if ins_size == outs_size:
            self.ids['apply_btn'].disabled = False
        else:
            self.ids['apply_btn'].disabled = True

    def reset(self):
        self.cells = {'inputs' : None, 'outputs': None}

        for table in ['inputs', 'outputs']:
            tbl = self.ids[f'{table}_tbl']
            tbl.clear_widgets()
            self.create_table(table)

        self.valid_to_apply()    
        self.resize()

    def resize(self):
        cells = self.cells
        size = [0, 0]
        tables = ['inputs', 'outputs']
        
        for table in tables:
            width = len(cells[table].columns) * 48
            self.ids[f'{table}_cont'].width = width
            size[0] += width
            height = len(cells[table].index)  * 48 + 48
            if height > size[1]: size[1] = height
        
        for table in tables:
            self.ids[f'{table}_cont'].height = size[1]
        
        self.ids.scroll_view.size = size

    def apply(self, *args):
        cells = self.cells
        truth_table = {}

        for table in ['inputs', 'outputs']:
            table_dict = {}

            for index, title_cell in enumerate(cells[table].columns[2:-1]):
                key = title_cell.text
                while len(key) < 3:
                    key = ' ' + key
                table_dict[key] = []

                jndex = index + 2
                for cell in cells[table].iloc[:-2, jndex].values:
                    value = cell.text
                    if value == 'X': value = None
                    else: value = int(value)
                    table_dict[key].append(value)

            truth_table[table] = DataFrame.from_dict(table_dict)

        self.get_ttbl(truth_table)
        self.cancel()

    def is_equal_signal(self, signal):
        if signal in self.signals: 
            return True
        else: 
            self.signals.append(signal)
            return False

    def erase_signal(self, signal):
        if signal in self.signals:
            self.signals.remove(signal)

    def write_column(self, instence, value):
        cells = self.cells[instence.cell_type]

        for cell in cells.iloc[:-2, instence.index]:
            cell.text = value
