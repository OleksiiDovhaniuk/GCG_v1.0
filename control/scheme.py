from copy import deepcopy
from random import random

from kivy.app import App
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

from control.lbl import Lbl
# from lbl import Lbl


class Scheme(FloatLayout):
    """ Class creats graphyc representation of the genotype.

    Methods:
        sign(signals),
        draw(number, genotype, height)
        pick_palette(number, start, stop)

    """
    SIGNALS_NUMBER = 6
    INPUTS= ['X', 'Y' , 'C1', 'al1', 'al2', 'al3', 'al4', 'al5', 'al6', 'al7', 'al8']
    OUTPUTS= ['S', 'C2' , 'P', 'gr1', 'gr2', 'gr3', 'gr4', 'gr5', 'gr6', 'gr7', 'gr8']
    GENOTYPE = [
        [32, 3], [0, 0], [4, 24], [0, 0], 
        [8, 3], [651, 20], [32, 12], [2, 17],
        [33, 20], [0, 0], [42, 17], [0, 0], 
        [0, 0], [0, 0], [1024, 3], [0, 0], 
        [7, 24], [0, 0], [4, 34], [1, 24]
    ]
    HEIGHT = 600

    def __init__(
        self, 
        height=HEIGHT, 
        inputs=INPUTS, 
        outputs=OUTPUTS, 
        genotype=GENOTYPE, 
        **kwargs
    ):
        """ The constructor draws scheme in kivy widget.

        Args:
            height [int, float],
            inputs: list of [str],
            outputs: list of [str],
            genotype: nested list.

        """
        super(Scheme, self).__init__(**kwargs) 
        self.size_hint = (None, 1)
        self.draw(
            height=height, 
            genotype=genotype,
            inputs=inputs, 
            outputs=outputs,
        )

    def sign(self, inputs, outputs):
        """ The method signs lines with responsible
        input`s and output`s names.

        Args:
            inputs: list of [str],
            outputs: list of [str].

        """
        lbl_height = self.step_y
        font_size  = .8 * self.step_y
        padding_y  = self.padding_y - (lbl_height / 2)

        pos = [[.2 * self.padding_x, padding_y + lbl_height * index] \
            for index in range(len(inputs))]
        for index, in_signal in enumerate(reversed(inputs)):
            self.add_widget(Lbl(
                text=in_signal,
                font_size=font_size,
                pos=pos[index],
                size_hint_y=None,
                height=lbl_height)
            )

        pos = [[self.width - .8 * self.padding_x, coord[1]]
            for coord in pos]
        for index, out_signal in enumerate(reversed(outputs)):
            self.add_widget(Lbl(
                text=out_signal,
                font_size=font_size,
                pos=pos[index],
                size_hint_y=None,
                height=lbl_height)
            )
    
    def draw(self, genotype, height, inputs, outputs):
        """ The method draws scheme according to genotype.
            
        Args: 
            genotype: nested list,
            height [int, float],
            inputs: list of [str],
            outputs: list of [str].

        """
        gnt = deepcopy(genotype)
        while [0, 0] in gnt:
            gnt.remove([0, 0])

        n_steps_y = len(inputs)  
        self.padding_y = padding_y = .1 * height
        self.step_y = step_y\
            = (height - 2 * padding_y) / (n_steps_y - 1)
        
        self.padding_x = padding_x = 2.5 * step_y
        n_steps_x = len(gnt) # n - from number
        self.width = width = step_y * 2 * (n_steps_x + 1)\
            + 2 * padding_x
        step_x = 2 * step_y

        line_width = step_y / 50
        palette    = self.pick_palette(n_steps_y)
        # coef of an angle of the switching singals  
        gate_unit  = step_x/2  # half of the gate width
        gate_pos   = []

        # calculate coordinates for getes on X-Axes 
        range_x = [padding_x + step_x * (index + 1) for index in range(n_steps_x+1)]
        # calculate coordinates for strate signal-lines in the scheme
        range_y = [height - padding_y - step_y * index for index in range(n_steps_y)]
        # the first points for lines of s scheme
        line_coords = [[padding_x, y, width-padding_x, y] for y in range_y]

        with self.canvas:
            # draw background
            Color(1, 1, 1, 1)
            Rectangle(size=(width, height), pos=(0,0))

            # draw signals-lines
            for index, line in enumerate(line_coords):
                Color(*palette[index])
                Line (
                    points=(line),
                    width=line_width,
                    cap='square',
                    joint='miter'
                )
            
            # draw circuits of the Fredkin gates 
            Color(0, 0, 0, 1)
            size_unit = .7 * gate_unit
            switch_width = 2* line_width
            for i, gene in enumerate(gnt):
                start_y = -1

                control = '{0:b}'.format(gene[0])
                while len(control) < n_steps_y:
                    control = '0' + control

                switch = '{0:b}'.format(gene[1])
                while len(switch) < n_steps_y:
                    switch = '0' + switch

                for j in range(n_steps_y):
                    # if bit in control bits is '1' draw control
                    if control[j] == "1":
                        Ellipse(
                            pos=(
                                range_x[i]-size_unit/2, 
                                range_y[j]-size_unit/2
                            ), 
                            size=(
                                size_unit,
                                size_unit
                            )
                        )
                        if start_y == -1: start_y = j

                    # if bit in switch bits is '1' draw switch
                    if switch[j] == "1":
                        Line(
                            points=(
                                range_x[i]-size_unit/2, 
                                range_y[j]-size_unit/2, 
                                range_x[i]+size_unit/2, 
                                range_y[j]+size_unit/2
                            ),
                            width=switch_width,
                            cap='square'
                        )
                        Line(
                            points=(
                                range_x[i]+size_unit/2, 
                                range_y[j]-size_unit/2, 
                                range_x[i]-size_unit/2, 
                                range_y[j]+size_unit/2
                            ),
                            width = switch_width,
                            cap   ='square'
                        )
                        if start_y == -1: start_y = j      

                end_y = n_steps_y
                for control_bit, switch_bit in zip(control[::-1], switch[::-1]):
                    end_y -= 1
                    if control_bit == '1' or switch_bit == '1':
                        break
                    
                # connection line
                Line(
                    points=(
                        range_x[i],
                        range_y[start_y],
                        range_x[i],
                        range_y[end_y]
                    ),
                    width = switch_width,
                    cap   ='square'
                )

        self.width = width
        self.sign(inputs, outputs)

    def pick_palette(self, number=SIGNALS_NUMBER):
        """ The method shoose semi-randomly pallete of coloures.

        Args: number [int].

        """
        palette = []

        index = 0
        while len(palette) < number: 
            colour = [0, 0, 0, 1]
            colour[index] = .4
            index = (index + 1) % 3
            colour[index] = random() * .4

            palette.append(colour)
        
        return palette

class SchemeDrawApp(App):
    def build(self):
        parent      = ScrollView(do_scroll_x=True, 
                                 effect_cls='ScrollEffect')
        self.parent = Scheme()
        parent.add_widget(self.parent)
        return parent

if __name__ == '__main__':
    SchemeDrawApp().run()
