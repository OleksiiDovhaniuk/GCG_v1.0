""" The module represents basis element of the circuits.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Date: 02.01.2021

:TODO: Finish Gate.save() method

"""

from PIL import Image, ImageFont, ImageDraw
from math import ceil


import numpy as np
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')


class Gate():
    """ The class defines circuit gate object.
        The constructor signs parameters to the gate object.

        :attr: title (str): An unique identifier for the gate.

        :attr: qcost (int): Quantum cost of the gate.

        :attr: delay (float): Delay of the gate in nano seconds.

        :attr: nodes (dict of string -> Node objects).

        :attr: size (int): Number of lines.

        :attr: mapping (numpy.ndarray):
            Numpy 2-dimansion array. It represents truth table of
            the gate.

        :attr: basis (int):
            Basis of the gate in range [2, ∞). By default, basis
            equals 2.

        :attr: _view_path (string, immutable).

        :attr: _min_width (int, immutable).

        :attr: _max_width (int, immutable).

        :attr: _default_width (int, immutable).

        :meth: get_view(width).

        :meth: save().

    """
    _view_path = '/res/gate/view/'
    _min_width = 8
    _max_width = 64
    _default_width = 32

    def __init__(self, tag, qcost, delay, nodes, mapping, basis=2):
        self.tag = tag
        self.qcost = max(qcost, 0)
        self.delay = max(delay, 0)
        self.nodes = nodes
        self.size = len(nodes)
        self.mapping = mapping
        self.basis = basis

    def get_view(self, width=_default_width):
        """ The function saves schematic view of the gate to file.

        :arg: file_name (string).

        :arg: width (int) width of the view in pixel.
        By default width = 64px. Min width walue 64px.

        :return: PIL Image object.

        """
        nodes = self.nodes

        width = int(ceil(min(max(width, self._min_width), self._max_width)))
        height = int(ceil((len(nodes) + (len(nodes)-1)*0.3) * width))
        step = int(width * 1.3)
        offset = int(width*0.2)
        size = (width + 2*offset, height)

        view = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(view)

        # Draw connecting line
        line_x = int(view.size[0] / 2)
        line_y = int(width / 2)
        line_width = int(view.size[0]/20)
        draw.line(xy=(line_x, line_y, line_x, view.size[1]-line_y),
                  fill=(0, 0, 0),
                  width=line_width)

        # Draw signal lines and nodes
        node_views = [node.get_view(a=width) for node in nodes]
        for i, node_view in enumerate(node_views):
            line_y = int(width/2) + i*step
            draw.line(xy=(0, line_y, width+2*offset, line_y),
                      fill=(0, 0, 0),
                      width=line_width)
            view.alpha_composite(node_view, (offset, i*step))

        return view

    def save(self):
        """ Method stores gate into database.

        """
        pass

    def __str__(self, view=1):
        """ The function defines how a class object
            will be printed in the console.

        """
        if view == 1:
            return f"{self.tag}"
        else:
            return f"{self.tag} gate characterises by \
                quantum cost = {self.qcost}, delay = {self.delay}. \
                The gate is gescribed in {self.basis}-bit basis."
