from ux.txtinput import TxtInput
from ux.btn import (
    PropertyDropDown,
    Btn,
)
from ux.layout import (
    ViewLayout,
    PropertyLayout,
    SubtitleLayout,
    Line1Dark,
    LightDefault,
)
from ux.lbl import Lbl
from math import floor
from functools import partial
import kivy
from kivy.uix.behaviors import ButtonBehavior
from ux.hoverBehaviour import HoverButton
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle
from kivy.properties import (
    StringProperty,
    NumericProperty,
    OptionProperty,
    ObjectProperty
)
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

kivy   .require('1.10.1')
Builder.load_file('ui/algorithmView.kv')


class AlgorithmView(ViewLayout):
    _properties = {'Genetic Algorithm': {
        'Sizes': {
            'Generation Size': 800,
            'Chromosome Size': 30,
            'Allele Size': 4,
            'Generation Memory Size': 3},
        'Crossover': {
            'Probability': .4,
            'Max Length': 30,
            # 'Crossover Fixed Length': True,
        },
        'Mutation': {
            'Probability': 0.08,
            'Max Length': 30,
            # 'Mutation Fixed Length': True,
        },
        'Stagnation': {
            'Coefficient': 10,
            'Solution': 'Island model',
            'Number of Islands': 4
        },
        'Coefficients': {
            'Error Coefficient': .97,
            'Disparity Coefficient': 0,
            'Quantum Cost Coefficient': .01,
            'Delay Coefficient': .01,
            'Garbage Outputs Coefficient': .01},
        'Limits': {
            'Number of Populations': 500,
            'Time Limit': None},
    },
        # 'Ant Colony': None,
    }

    DEF_COEFS = {
        'Hamming Dist. Coefficient': ['float', 0, float('+inf'), None],
        'Disparity Coefficient': ['float', 0, float('+inf'), None],
        'Quantum Cost Coefficient': ['float', 0, float('+inf'), None],
        'Delay Coefficient': ['float', 0, float('+inf'), None],
        'Ancillary Bits Coefficient': ['float', 0, float('+inf'), None],
        'TCL Coefficient': ['float', 0, float('+inf'), None],
    }

    def __init__(self):
        ViewLayout.__init__(self, 'Algorithm')
        syn_ga = GeneticAlgorithmSpecs(key='Synthesis')
        sythesis_specs = BoxTitle(
            label='Synthesis algorithm:',
            options=[
                'Genetic Algorithm',
                # 'Ant Colony',
            ],
            state='Genetic Algorithm',
            content=[
                syn_ga,
                # Lbl(text='<Placeholder>: Functionality in progress!'),
            ],
        )
        syn_island_model = IslandModelSpecs(
            syn_ga.ids.gen_size,
            syn_ga.ids.chrm_size,
            key='Synthesis',
        )
        syn_postga = PostGASpecs(
            syn_ga.ids.gen_size,
            syn_ga.ids.chrm_size,
        )
        synthesis_stagnation = BoxTitle(
            label='Stagnation handler:',
            options=['Island Model', 'PostGA'],
            state='Island Model',
            content=[
                syn_island_model,
                syn_postga,
            ],
            list_width=200,
        )
        syn_migration = BoxTitle(
            label='Migration type:',
            options=['Best Individuals', 'Worst Individuals', 'Random'],
            state='Best Individuals',
            list_width=200,
        )
        syn_island_model.ids.migration_type.add_widget(syn_migration)
        syn_ga.ids.stagnation.bind(
            minimum_height=syn_ga.ids.stagnation.setter('height'))
        syn_ga.ids.stagnation.add_widget(synthesis_stagnation)
        optimization_specs = BoxTitle(
            label='Optimization algorithm:',
            options=[
                'None',
                'Use Synthesis Algorithm',
                # 'Genetic Algorithm',
                # 'Ant Colony'
            ],
            state='Use Synthesis Algorithm',
            content=[
                BoxLayout(size_hint_y=None, height=0),
                BoxLayout(size_hint_y=None, height=0),
                # GeneticAlgorithmSpecs(key='Optimization'),
                # Lbl(text='<Placeholder>: Functionality in progress!'),
            ],
        )
        # iteration_no = DigitSpec(label='Iteration No.:')
        # iteration_no.value = 100
        # iteration_no.default = 100
        # iteration_no.min_value = 10

        # time_limit = DigitSpec(label='Time (in sec.):')
        # time_limit.value = 60
        # time_limit.default = 60
        # time_limit.min_value = 10

        termination_specs = BoxTitle(
            label='Termination condition:',
            options=['Iteration No.', 'Time'],
            state='Iteration No.',
            content=[IterationNoSpecs(), TimeLimitSpecs()],
        )

        self.add_widget(sythesis_specs)
        self.add_widget(SpecsSeparator())
        self.add_widget(optimization_specs)
        self.add_widget(SpecsSeparator())
        self.add_widget(termination_specs)


class BoxTitle(BoxLayout):
    label = StringProperty('<Placeholder>: label')
    options = []
    state = StringProperty()
    content = []
    list_width = NumericProperty(629)

    def __init__(self, options, state, content=None, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        box = self.ids.box
        self.bind(minimum_height=self.setter('height'))
        box.bind(minimum_height=box.setter('height'))
        if content:
            self.ids.list_specs.fill_content(content, box)
        else:
            self.remove_widget(box)
        self.ids.list_specs.fill_list(options, state)


class ListSpecs(HoverButton):
    btns = []
    content = None
    box = BoxLayout()

    def __init__(self, *args, **kwargs):
        HoverButton.__init__(self, *args, **kwargs)
        self.dropdown = DropDownSpecs(self)

    def open_list(self):
        self.dropdown.open(self)
        self.disabled = True

    def fill_list(self, labels, state=None):
        btns = self.btns = []
        if not state:
            state = labels[0]
        for lbl in labels:
            btns.append(ListBtn(text=lbl))
            btns[-1].bind(on_release=self.select)
            self.dropdown.add_widget(btns[-1])
            if state == lbl:
                self.select(btns[-1])

    def fill_content(self, content, box):
        self.box = box
        self.content = content

    def select(self, button):
        self.text = button.text
        self.dropdown.select(button)
        for btn in self.btns:
            btn.disabled = False
        button.disabled = True
        if self.content:
            self.box.clear_widgets()
            self.box.add_widget(self.content[self.btns.index(button)])


class DropDownSpecs(DropDown):
    def __init__(self, parnt, *args, **kwargs):
        DropDown.__init__(self, *args, **kwargs)
        self.parnt = parnt

    def on_dismiss(self):
        self.parnt.disabled = False


class ListBtn(HoverButton):
    pass


class GeneticAlgorithmSpecs(BoxLayout):
    groups = {}

    def __init__(self, key):
        super().__init__()
        self.bind(minimum_height=self.setter('height'))
        for key in self.groups:
            self.recalc_group(self.groups[key][0])

    def group_up(self, instance, *args):
        key = f'{self}/{instance.group}'
        if key in self.groups:
            self.groups[key].append(instance)
        else:
            self.groups[key] = [instance]
        instance.bind(value=self.recalc_group)

    def recalc_group(self, instance, *args):
        key = f'{self}/{instance.group}'
        values = [spec.value for spec in self.groups[key]]
        total = sum(values)
        for inst in self.groups[key]:
            inst.ids.segment.text = f'{floor(inst.value/total*100)}%'


class PostGASpecs(BoxLayout):
    groups = {}
    gen_size = ObjectProperty()
    chrm_size = ObjectProperty()

    def __init__(self, gen_size, chrm_size, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.bind(minimum_height=self.setter('height'))
        self.ids.box.bind(minimum_height=self.ids.box.setter('height'))
        self.ids.specs.bind(minimum_height=self.ids.specs.setter('height'))
        self.ids.left_specs.bind(
            minimum_height=self.ids.left_specs.setter('height'))
        self.ids.right_specs.bind(
            minimum_height=self.ids.right_specs.setter('height'))

        self.gen_size = gen_size
        self.chrm_size = chrm_size

        for key in self.groups:
            self.recalc_group(self.groups[key][0])

    def group_up(self, instance, *args):
        key = f'{self}/{instance.group}'
        if key in self.groups:
            self.groups[key].append(instance)
        else:
            self.groups[key] = [instance]
        instance.bind(value=self.recalc_group)

    def recalc_group(self, instance, *args):
        key = f'{self}/{instance.group}'
        values = [spec.value for spec in self.groups[key]]
        total = sum(values)
        for inst in self.groups[key]:
            inst.ids.segment.text = f'{floor(inst.value/total*100)}%'


class IslandModelSpecs(BoxLayout):
    MAX_ISLANDS = 5
    islands = []
    gen_size = ObjectProperty()
    chrm_size = ObjectProperty()
    groups = {}
    key = StringProperty()

    def __init__(self, gen_size, chrm_size, key, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        box = self.ids.box
        self.bind(minimum_height=self.setter('height'))
        box.bind(minimum_height=box.setter('height'))
        self.key = key

        self.add_island()

        self.gen_size = gen_size
        self.chrm_size = chrm_size

        for key in self.groups:
            self.recalc_group(self.groups[key][0])

    def group_up(self, instance, *args):
        key = f'{self.key}/{instance.group}'
        if key in self.groups:
            self.groups[key].append(instance)
        else:
            self.groups[key] = [instance]
        instance.bind(value=self.recalc_group)

    def recalc_group(self, instance, *args):
        key = f'{self.key}/{instance.group}'
        values = [spec.value for spec in self.groups[key]]
        total = sum(values)
        for inst in self.groups[key]:
            inst.ids.segment.text = f'{floor(inst.value/total*100)}%'

    def add_island(self):
        islands_no = len(self.islands)
        if islands_no < self.MAX_ISLANDS:
            self.islands.append(IslandSpecs(
                self.gen_size,
                self.chrm_size,
                set_index=islands_no+1,
                islands_group_up=self.group_up,
            ))
            self.islands[-1].ids.del_btn.bind(on_press=self.del_island)
            self.ids.box.add_widget(self.islands[-1])
            self.recalc_group(self.islands[-1].ids.island_weight)

            if islands_no == 1:
                self.islands[0].ids.del_btn.disabled = False
            elif islands_no == 4:
                self.ids.add_btn.disabled = True

    def del_island(self, button, *args):
        islands_no = len(self.islands)
        if islands_no > 1:
            island = button.content
            self.islands.remove(island)
            self.ids.box.remove_widget(island)
            self.groups[f'{self.key}/Islands'].remove(island.ids.island_weight)
            self.recalc_group(island.ids.island_weight)

            for index, islnd in enumerate(self.islands):
                islnd.ids.title.text = f'Island #{index+1}:'

            if islands_no == 2:
                self.islands[0].ids.del_btn.disabled = True
            elif islands_no == 5:
                self.ids.add_btn.disabled = False


class IslandSpecs(BoxLayout):
    set_index = NumericProperty(1)
    groups = {}
    gen_size = ObjectProperty()
    chrm_size = ObjectProperty()

    def __init__(self, gen_size, chrm_size, islands_group_up, *args, **kwargs):
        self.gen_size = gen_size
        self.chrm_size = chrm_size
        self.islands_group_up = islands_group_up

        BoxLayout.__init__(self, *args, **kwargs)

        self.bind(minimum_height=self.setter('height'))
        self.ids.specs.bind(minimum_height=self.ids.specs.setter('height'))
        self.ids.left_specs.bind(
            minimum_height=self.ids.left_specs.setter('height'))
        self.ids.right_specs.bind(
            minimum_height=self.ids.right_specs.setter('height'))

        for key in self.groups:
            self.recalc_group(self.groups[key][0])

    def group_up(self, instance, *args):
        key = f'{self}/{instance.group}'
        if key in self.groups:
            self.groups[key].append(instance)
        else:
            self.groups[key] = [instance]
        instance.bind(value=self.recalc_group)

    def recalc_group(self, instance, *args):
        key = f'{self}/{instance.group}'
        values = [spec.value for spec in self.groups[key]]
        total = sum(values)
        for inst in self.groups[key]:
            inst.ids.segment.text = f'{floor(inst.value/total*100)}%'

    def del_status(self):
        return self.set_index == 1


class DigitSpec(BoxLayout):
    TYPES = ('int', 'float')
    label = StringProperty('<Placeholder>: label')
    default = NumericProperty(-1)
    value = NumericProperty(-1)
    min_value = NumericProperty(float('-inf'))
    max_value = NumericProperty(float('+inf'))
    min_bind = ObjectProperty()
    max_bind = ObjectProperty()
    value_type = StringProperty('float')
    input_width = NumericProperty(200)

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.bind(value=self.show_value)
        self.bind(default=self.show_default)

    def set_type(self, value_type):
        if value_type in self.TYPES:
            self.value_type = value_type
        else:
            self.value_type = 'int'

    def show_value(self, *args):
        self.ids.input.text = str(self.value)

    def show_default(self, *args):
        self.ids.input.hint_text = str(self.default)

    def validate(self, *args):
        txt_input = self.ids.input
        if not txt_input.focus:
            try:
                new_value = float(txt_input.text)
            except ValueError:
                new_value = self.value

            if self.min_bind:
                if new_value < self.min_bind.value:
                    new_value = self.value
            if self.max_bind:
                if new_value > self.max_bind.value:
                    new_value = self.value
            if new_value < self.min_value or new_value > self.max_value:
                new_value = self.value

            if self.value_type == 'int':
                self.value = int(new_value)
            else:
                self.value = new_value
            txt_input.text = str(self.value)


class DigitInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if substring == '-':
            s = ''
        else:
            s = substring
        return TextInput.insert_text(self, s, from_undo=from_undo)


class SpecsSeparator(BoxLayout):
    pass


class WeightSpec(DigitSpec):
    part = NumericProperty(0)
    group = StringProperty()
    segment_color_hex = StringProperty('#56CCF2')


class DelBtn(Btn):
    content = ObjectProperty()


class IterationNoSpecs(BoxLayout):
    def __init__(self):
        super().__init__()
        self.bind(minimum_height=self.setter('height'))


class TimeLimitSpecs(BoxLayout):
    def __init__(self):
        super().__init__()
        self.bind(minimum_height=self.setter('height'))
