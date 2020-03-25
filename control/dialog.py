from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from control.cell import Cell, EmptyCell, TitleCell, AddCell, IndexCell
from control.layout import TTblRow

from pandas import DataFrame
from functools import partial
from design import Design


Builder.load_file('view/dialog.kv')

class Dialog(FloatLayout):
    theme = Design().default_theme
    cancel = ObjectProperty(None)

class Load(Dialog):
    load = ObjectProperty(None)

class Save(Dialog):
    save = ObjectProperty(None)
    data = ObjectProperty(None)

class TruthTable(Dialog):
    apply = ObjectProperty(None)
    reset = ObjectProperty(None)
    truth_table = ObjectProperty(None)
    cells = {'inputs': [], 'outputs': []}

    def __init__(self, truth_table, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.truth_table = truth_table
        self.create_table('inputs')
        self.create_table('outputs')
        self.resize()
        
    def create_table(self, table):
        values = self.truth_table[table].replace([None], 'X')
        tbl = self.ids[f'{table}_tbl']    
        row = TTblRow() 
        row.add_widget(EmptyCell())
        key_widgets = [row, 'indices']
        for index, key in enumerate(values):
            cell = TitleCell(text=key, 
                        cell_type=table,
                        index=index+2,
                        remove_column = self.remove_column)
            row.add_widget(cell)
            key_widgets.append(cell)
        add_cell_column = AddCell()
        row.add_widget(add_cell_column)
        key_widgets.append(add_cell_column)
        tbl.add_widget(row)
        widgets = []
        indices = [0, 1]
        for index in range(values.shape[0]):
            row = TTblRow() 
            index_cell = IndexCell(index=str(index))
            row.add_widget(index_cell)
            row_widgets = [row, index_cell]
            for key in values:
                value = values[key][index]
                cell = Cell(text=str(value), cell_type=table)
                row.add_widget(cell)
                row_widgets.append(cell)
            tbl.add_widget(row)
            indices.append(index+1)
            widgets.append(row_widgets)
        row = TTblRow()
        add_cell = AddCell()
        row.add_widget(add_cell)
        tbl.add_widget(row)
        row_widgets = [None for _ in range(len(key_widgets))]
        row_widgets[0] = row
        row_widgets[1] = add_cell
        widgets.append(row_widgets)
        align_lt = BoxLayout()
        tbl.add_widget(align_lt)
        row_widgets = [None for _ in range(len(key_widgets))]
        row_widgets[0] = align_lt
        widgets.append(row_widgets)
        self.cells[table] = DataFrame(data=widgets,
                                index=indices,
                                columns=key_widgets)
        for index, cell in enumerate(self.cells[table]['indices'][:len(indices)-2]):
            cell.bind(on_release=partial(self.remove_row, table, int(cell.index)))
        add_cell.bind(on_release=partial(self.add_row, table))

        add_cell_column.bind(on_release=partial(self.add_column, table))

    def remove_row(self, table, index, *args):
        tbl = self.ids[f'{table}_tbl']
        cells = self.cells[table] 
        columns = cells.columns
        size = len(cells.index)
        last_cell_index = len(columns)-1

        new_cells_part1 = DataFrame(columns=columns)
        new_cells_part1 =  new_cells_part1.append(cells.iloc[:index, :])

        rows = cells.iloc[index:, 0].values
        for row in rows:
            tbl.remove_widget(row)

        rows = cells.iloc[index+1: size-2, 0].values
        widgets = []
        for jndex, row in enumerate(rows):
            kndex = index + jndex
            new_row = TTblRow()
            new_index_cell = IndexCell(index = str(cells.iloc[kndex, 1].index))
            row_widgets = [new_row, new_index_cell]
            new_row.add_widget(new_index_cell)
            for cell in cells.iloc[kndex+1, 2:last_cell_index].values:
                new_cell = Cell(text=cell.text, cell_type=table)
                new_row.add_widget(new_cell)
                row_widgets.append(new_cell)
            tbl.add_widget(new_row)
            widgets.append(row_widgets)

        row = TTblRow()
        tbl.add_widget(row)
        add_cell = AddCell()
        row.add_widget(add_cell)
        row_widgets = [None for _ in range(len(columns))]
        row_widgets[0] = row
        row_widgets[1] = add_cell
        widgets.append(row_widgets)

        align_lt = BoxLayout()
        tbl.add_widget(align_lt)
        row_widgets = [None for _ in range(len(columns))]
        row_widgets[0] = align_lt
        widgets.append(row_widgets)

        new_indices = [jndex for jndex in range(index, size-1)]
        new_cells_part2 = DataFrame(data=widgets, columns=columns, index=new_indices)
        self.cells[table] = new_cells_part1.append(new_cells_part2)
        for index, cell in enumerate(new_cells_part2['indices'][:len(new_indices)-2]):
            cell.bind(on_release=partial(self.remove_row, table, int(cell.index)))
        add_cell.bind(on_release=partial(self.add_row, table))
        self.resize()

    def add_row(self, table, *args):
        tbl = self.ids[f'{table}_tbl']
        cells = self.cells[table] 
        columns = cells.columns
        row_size = len(columns)
        del_index = len(cells.index) - 2

        new_cells_part1 = DataFrame(columns=columns)
        new_cells_part1 =  new_cells_part1.append(cells.iloc[:del_index, :])

        rows = cells.iloc[del_index:, 0].values
        for row in rows:
            tbl.remove_widget(row)

        row = TTblRow()
        index_cell = IndexCell(index=str(del_index))
        row_widgets = [row, index_cell]
        row.add_widget(index_cell)
        for index in range(row_size-3):
            cell = Cell(text='0', cell_type=table)
            row.add_widget(cell)
            row_widgets.append(cell)
        tbl.add_widget(row)
        widgets = [row_widgets]

        row = TTblRow()
        tbl.add_widget(row)
        add_cell = AddCell()
        row.add_widget(add_cell)
        row_widgets = [None for _ in range(row_size)]
        row_widgets[0] = row
        row_widgets[1] = add_cell
        widgets.append(row_widgets)

        align_lt = BoxLayout()
        tbl.add_widget(align_lt)
        row_widgets = [None for _ in range(row_size)]
        row_widgets[0] = align_lt
        widgets.append(row_widgets)

        new_indices = [index for index in range (del_index, del_index + 3)]
        new_cells_part2 = DataFrame(data=widgets, columns=columns, index=new_indices)
        self.cells[table] = new_cells_part1.append(new_cells_part2)
        for index, cell in enumerate(new_cells_part2['indices'][:len(new_indices)-2]):
            cell.bind(on_release=partial(self.remove_row, table, int(cell.index)))
        add_cell.bind(on_release=partial(self.add_row, table))
        self.resize()

    def remove_column(self, table, index, *args):
        cells = self.cells[table] 
        column_size = len(cells.index) - 2
        columns = cells.columns

        columns[0].remove_widget(columns[index])
        for jndex, row in enumerate(cells.iloc[:column_size, 0].values):
            row.remove_widget(cells.iloc[jndex, index])

        self.cells[table] = self.cells[table].drop(columns=[columns[index]])
        self.resize()

    def add_column(self, table, *args):
        cells = self.cells[table] 
        columns = cells.columns
        add_index = len(columns) - 1
        column_size = len(cells.index) - 2
        
        columns[0].remove_widget(columns[add_index])
        key_cell = TitleCell(index=add_index,
                        cell_type=table,
                        remove_column=self.remove_column)
        columns[0].add_widget(key_cell)
        key_cell.focus = True
        columns[0].add_widget(columns[add_index])

        column_widgets = []
        for index in range(column_size):
            cell = Cell(text='0', cell_type=table)
            cells.iloc[index, 0].add_widget(cell)
            column_widgets.append(cell)
        for _ in range(2):
            column_widgets.append(None)

        self.cells[table].insert(add_index, key_cell, column_widgets, False)
        self.resize()
        
    def reset(self):
        self.cells = {'inputs': None, 'outputs': None}
        tbl = self.ids['inputs_tbl']
        tbl.clear_widgets()
        self.create_table('inputs')
        tbl = self.ids['outputs_tbl']
        tbl.clear_widgets()
        self.create_table('outputs')  
        self.resize()

    def resize(self):
        cells = self.cells
        size = [0, 0]
        tables = ['inputs', 'outputs']
        
        for table in tables:
            width = len(cells[table].columns) * 48 + 48
            self.ids[f'{table}_cont'].width = width
            size[0] += width
            height = len(cells[table].index)  * 48 + 48
            if height > size[1]: size[1] = height
        
        for table in tables:
            self.ids[f'{table}_cont'].height = size[1]
        
        self.ids.scroll_view.size = size