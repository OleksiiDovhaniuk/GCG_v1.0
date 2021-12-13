from copy import deepcopy
from random import random

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

# from ux.lbl import Lbl

from lbl import Lbl
from component.node import Node
from component.gate import Gate

Builder.load_file('scheme.kv')


class SchemeLabel(Lbl):
    STYPES = ('input', 'output')

    def __init__(self, text=None, stype=None):
        """ The class represents cells of a drawing scheme with labels.

            :arg: `text` (str): Text of the label.

            :arg: `stype` ('input' or 'output'): Represents a type of the 
                signal which is signed.

            :note: if `stype` is not entered, the object is usually used for
                signing gates on the scheme. If `text` and `stype` are not 
                specified, SchemeLabel can be used as a space holder. 

        """
        if isinstance(text, str):
            Lbl.__init__(self, text=text)
        else:
            Lbl.__init__(self, text='')

        if stype in self.STYPES:
            self.stype = stype
        else:
            self.stype = None


class Scheme(BoxLayout):
    def __init__(self, scheme, signals):
        """ The class represents visualization of the scheme in kivy widget.

            :arg: `scheme` (list of gates): The scheme schould be cleaned from 
                null gates.

            :arg: `signals` (2D list of str): Ordered labels of the signals.

        """
        BoxLayout.__init__(self)
        

    # class Scheme(FloatLayout):
    #     """ Class creats graphyc representation of the genotype.

    #     Methods:
    #         sign(signals),
    #         draw(number, genotype, height)
    #         pick_palette(number, start, stop)

    #     """
    #     HEIGHT = 600

    #     def __init__(self, signals, genotype, height=HEIGHT, **kwargs):
    #         """ The constructor draws scheme in kivy widget.

    #         :arg: `signals` (nested list). List of paares of signals titles: [input, output]

    #         :arg: `genotype` (list of chms).

    #         :arg: `height` (int). Hight of the scheme in px.

    #         """
    #         super(Scheme, self).__init__(**kwargs)
    #         self.size_hint = (None, 1)
    #         self._draw(signals, genotype, height)

    #     def _draw(self, signals, genotype, height):
    #         """ The method draws scheme according to genotype.

    #         :arg: `signals` (nested list). List of paares of signals titles: [input, output]

    #         :arg: `genotype` (list of chms).

    #         :arg: `height` (int). Hight of the scheme in px.

    #         """
    #         gnt = [al for al in genotype if al[0].tag != 'None']

    #         n_steps_y = len(signals)
    #         self.padding_y = padding_y = .1 * height
    #         self.step_y = step_y\
    #             = (height - 2 * padding_y) / (n_steps_y - 1)

    #         self.padding_x = padding_x = 2.5 * step_y
    #         n_steps_x = len(gnt)  # n - from number
    #         self.width = width = step_y * 2 * (n_steps_x + 1)\
    #             + 2 * padding_x
    #         step_x = 2 * step_y

    #         line_width = step_y / 50
    #         palette = self.pick_palette(n_steps_y)
    #         gate_unit = step_x/2  # half of the gate width
    #         gate_pos = []

    #         # calculate coordinates for getes on X-Axes
    #         range_x = [padding_x + step_x * (index + 1)
    #                    for index in range(n_steps_x+1)]
    #         # calculate coordinates for strate signal-lines in the scheme
    #         range_y = [height - padding_y - step_y *
    #                    index for index in range(n_steps_y)]
    #         # the first points for lines of s scheme
    #         line_coords = [[padding_x, y, width-padding_x, y] for y in range_y]

    #         with self.canvas:
    #             # draw background
    #             Color(1, 1, 1, 1)
    #             Rectangle(size=(width, height), pos=(0, 0))

    #             # draw signals-lines
    #             for index, line in enumerate(line_coords):
    #                 Color(*palette[index])
    #                 Line(
    #                     points=(line),
    #                     width=line_width,
    #                     cap='square',
    #                     joint='miter'
    #                 )

    #             # draw circuits of the Fredkin gates
    #             Color(0, 0, 0, 1)
    #             size_unit = .7 * gate_unit
    #             switch_width = 2 * line_width
    #             for i, gene in enumerate(gnt):
    #                 start_y = -1

    #                 control = '{0:b}'.format(gene[0])
    #                 while len(control) < n_steps_y:
    #                     control = '0' + control

    #                 switch = '{0:b}'.format(gene[1])
    #                 while len(switch) < n_steps_y:
    #                     switch = '0' + switch

    #                 for j in range(n_steps_y):
    #                     # if bit in control bits is '1' draw control
    #                     if control[j] == "1":
    #                         Ellipse(
    #                             pos=(
    #                                 range_x[i]-size_unit/2,
    #                                 range_y[j]-size_unit/2
    #                             ),
    #                             size=(
    #                                 size_unit,
    #                                 size_unit
    #                             )
    #                         )
    #                         if start_y == -1:
    #                             start_y = j

    #                     # if bit in switch bits is '1' draw switch
    #                     if switch[j] == "1":
    #                         Line(
    #                             points=(
    #                                 range_x[i]-size_unit/2,
    #                                 range_y[j]-size_unit/2,
    #                                 range_x[i]+size_unit/2,
    #                                 range_y[j]+size_unit/2
    #                             ),
    #                             width=switch_width,
    #                             cap='square'
    #                         )
    #                         Line(
    #                             points=(
    #                                 range_x[i]+size_unit/2,
    #                                 range_y[j]-size_unit/2,
    #                                 range_x[i]-size_unit/2,
    #                                 range_y[j]+size_unit/2
    #                             ),
    #                             width=switch_width,
    #                             cap='square'
    #                         )
    #                         if start_y == -1:
    #                             start_y = j

    #                 end_y = n_steps_y
    #                 for control_bit, switch_bit in zip(control[::-1], switch[::-1]):
    #                     end_y -= 1
    #                     if control_bit == '1' or switch_bit == '1':
    #                         break

    #                 # connection line
    #                 Line(
    #                     points=(
    #                         range_x[i],
    #                         range_y[start_y],
    #                         range_x[i],
    #                         range_y[end_y]
    #                     ),
    #                     width=switch_width,
    #                     cap='square'
    #                 )

    #         self.width = width
    #         self.sign(sign_inputs, self.order_outputs(
    #             genotype, line_no, inputs, outputs))

    #     def _sign(self, line_no, signals, genotype):
    #         """ The method signs lines with responsible
    #         input`s and output`s names.

    #         :arg: `line_no` (int).

    #         :arg: `signals` (nested list). List of paares of signals titles: [input, output]

    #         :arg: `genotype` (list of chms).

    #         """
    #         lbl_height = self.step_y
    #         font_size = .8 * self.step_y
    #         padding_y = self.padding_y - (lbl_height / 2)

    #         pos = [[.2 * self.padding_x, padding_y + lbl_height * index]
    #                for index in range(len(inputs))]
    #         for index, in_signal in enumerate(reversed(inputs)):
    #             self.add_widget(Lbl(
    #                 text=in_signal,
    #                 font_size=font_size,
    #                 pos=pos[index],
    #                 size_hint_y=None,
    #                 height=lbl_height)
    #             )

    #         pos = [[self.width - .8 * self.padding_x, coord[1]]
    #                for coord in pos]
    #         for index, out_signal in enumerate(reversed(outputs)):
    #             self.add_widget(Lbl(
    #                 text=out_signal,
    #                 font_size=font_size,
    #                 pos=pos[index],
    #                 size_hint_y=None,
    #                 height=lbl_height)
    #             )

    #     def _order_outputs(self, genotype, line_no, inputs, outputs):
    #         """ The method orderes outputs for according scheme and
    #         adds notes to the (e.i. number of errors, output signals).

    #         Args:
    #             genotype: nested list,
    #             line_no: [int],
    #             inputs: dictionary,
    #             outputs: dictionary.

    #         Returns:
    #             inputs: ordered inputs;
    #             outputs: ordered outputs;
    #             notes: ordered notes.

    #         """
    #         order = []
    #         errors = []
    #         chromosome = [gene for gene in genotype if gene != [0, 0]]
    #         output_values = self.prep_signals(outputs, is_ins=False)
    #         input_values = self.prep_signals(inputs)
    #         out_no = len(output_values[0])
    #         err_list = [[0] * line_no for _ in range(out_no)]
    #         err_no = 0

    #         for ins, outs in zip(input_values, output_values):
    #             for control, switch in chromosome:
    #                 if control & ins == control:
    #                     if '{0:b}'.format(switch & ins).count('1') == 1:
    #                         ins = ins ^ switch

    #             str_ins = '{0:b}'.format(ins)
    #             while len(str_ins) < line_no:
    #                 str_ins = '0' + str_ins

    #             for i in range(len(outs)):
    #                 for j in range(line_no):
    #                     err_list[i][j] += outs[i] ^ int(str_ins[j])

    #         unreachable_value = len(err_list)*out_no + 999
    #         for i in range(out_no):
    #             min_err_global = unreachable_value

    #             for j in range(err_list):
    #                 min_err = err_list[j].min()
    #                 if min_err < min_err_global:
    #                     min_err_global = min_err
    #                     index_x = err_list.index(min_err)
    #                     index_y = j

    #             order.append([index_x, index_y])
    #             errors.append(min_err_global)

    #             for i in range(err_list[index_y]):
    #                 err_list[index_y][i] = unreachable_value

    #             for i in range(err_list):
    #                 err_list[i][index_x] = unreachable_value

    #         ordered_outputs = ['grb.' for _ in range(len(err_list))]
    #         output_titles = [title for title in outputs]
    #         input_title = [title for title in inputs]

    #         for paar in order:
    #             pass
    #         """
    #         !!!!!!!!!!!!!!!!!!!!!!!!!!!! CODE HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #         """
    #         """
    #         !!!!!!!!!!!!!!!!!!!!!!!!!!!! CODE HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #         """
    #         """
    #         !!!!!!!!!!!!!!!!!!!!!!!!!!!! CODE HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #         """

    #         return input_title, errors

    #     def _prep_signals(self, signals, is_ins=True):
    #         """ The method converts signals of dictionary into list.

    #         Args:
    #             signals: dictionary {<signal_title>: <values>}.
    #             is_ins: is the inputed dictionary of input signals (by default TRUE).

    #         Returns:
    #             prep_signals: list of the integers related to the inputed signals.

    #         """
    #         if is_ins:
    #             return [int(signals[title], 2) for title in signals]
    #         else:
    #             return list(map(list, zip(*[[int(signal) for signal in signals[title]] for title in signals])))

    #     def _pick_palette(self, number=SIGNALS_NUMBER):
    #         """ The method shoose semi-randomly pallete of coloures.

    #         Args: number [int].

    #         """
    #         palette = []

    #         index = 0
    #         while len(palette) < number:
    #             colour = [0, 0, 0, 1]
    #             colour[index] = .4
    #             index = (index + 1) % 3
    #             colour[index] = random() * .4

    #             palette.append(colour)

    #         return palette


class SchemeDrawApp(App):
    def build(self):
        FG = Gate(
            tag='FG',
            qcost=5,
            delay=5,
            nodes={
                'Control': Node('__circle_black'),
                'Target1': Node('__cross'),
                'Target2': Node('__cross')},
            mapping=[
                [0, 0, 0],
                [1, 0, 0],
                [0, 1, 0],
                [1, 0, 1],
                [0, 0, 1],
                [1, 1, 0],
                [0, 1, 1],
                [1, 1, 1]])
        NONEG = Gate(
            tag='None',
            qcost=0,
            delay=0,
            nodes={'None': Node('__dot_white_triangle_down')},
            mapping=[[0], [1]])
        SCHEME = [
            [FG, [0, 4, 3]],
            [FG, [1, 0, 2]],
            [FG, [0, 3, 2]],
            [FG, [3, 0, 1]],
            [FG, [2, 0, 3]]]
        SIGNALS = [
            ['X', 'Y', 'Cin', '1', '0'],
            ['S', 'Cout', 'g0', 'g1', 'g2']]

        parent = ScrollView(
            do_scroll_x=True,
            effect_cls='ScrollEffect'
        )
        self.parent = Scheme(SCHEME, SIGNALS)
        parent.add_widget(self.parent)
        return parent


if __name__ == '__main__':
    SchemeDrawApp().run()
