""" The module is designed to test the Gate class.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Date: 05.01.2021

:TODO: Write code sample for TestGate.test_save() method.

"""
from PIL import Image
from component.gate import Gate
from component.node import Node
import unittest
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')


class TestGate(unittest.TestCase):

    def setUp(self):
        n1 = Node('__dot_black')
        n2 = Node('__cross')
        n3 = Node('__circle_crossed')
        n4 = Node('__dot_white')

        # 1. Negation gate
        self.nodes1 = [n3]
        self.map1 = [[1], [0]]
        self.g1 = Gate('NOT2b', 1, 1, self.nodes1, self.map1)

        # 2. Negative Control Not gate
        self.nodes2 = [n4, n3]
        self.map2 = [[0, 1], [0, 0], [1, 0], [1, 1]]
        self.g2 = Gate('NCN2b', 3, 2, self.nodes2, self.map2)

        # 3. Fredkin gate
        self.nodes3 = [n1, n2, n2]
        self.map3 = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                     [1, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1]]
        self.g3 = Gate('FRG2b', 5, 1.92, self.nodes3, self.map3)

        # 4. Toffoli gate
        self.nodes4 = [n1, n1, n3]
        self.map4 = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                     [1, 0, 0], [1, 0, 1], [1, 1, 1], [1, 1, 0]]
        self.g4 = Gate('TG2b', 5, 1.5, self.nodes4, self.map4)

    def tearDown(self):
        """ The function is called after each test function is executed.

        If there are connections are needed to enject, 
        then enter appropriate code below.

        """
        for gate in (self.g1, self.g2, self.g3, self.g4):
            for node in gate.nodes:
                node.icon.close()

    def test__init__(self):
        g1 = self.g1
        g2 = self.g2
        g3 = self.g3
        g4 = self.g4

        self.assertEqual(g1.tag, 'NOT2b')
        self.assertEqual(g2.tag, 'NCN2b')
        self.assertEqual(g3.tag, 'FRG2b')
        self.assertEqual(g4.tag, 'TG2b')

        self.assertEqual(g1.qcost, 1)
        self.assertEqual(g2.qcost, 3)
        self.assertEqual(g3.qcost, 5)
        self.assertEqual(g4.qcost, 5)

        self.assertEqual(g1.delay, 1)
        self.assertEqual(g2.delay, 2)
        self.assertEqual(g3.delay, 1.92)
        self.assertEqual(g4.delay, 1.5)

        self.assertEqual(g1.nodes, self.nodes1)
        self.assertEqual(g2.nodes, self.nodes2)
        self.assertEqual(g3.nodes, self.nodes3)
        self.assertEqual(g4.nodes, self.nodes4)

        self.assertEqual(g1.size, 1)
        self.assertEqual(g2.size, 2)
        self.assertEqual(g3.size, 3)
        self.assertEqual(g4.size, 3)

        self.assertEqual(g1.mapping, self.map1)
        self.assertEqual(g2.mapping, self.map2)
        self.assertEqual(g3.mapping, self.map3)
        self.assertEqual(g4.mapping, self.map4)

    def test_get_view(self):
        view1 = self.g1.get_view()
        view2 = self.g2.get_view(4)
        view3 = self.g3.get_view(24)
        view4 = self.g4.get_view(512)

        with Image.open(f'res/node/__circle_crossed.png') as img:
            test_img_type = type(img.resize((64, 64)))

            self.assertEquals(type(view1), test_img_type)
            self.assertEquals(type(view2), test_img_type)
            self.assertEquals(type(view3), test_img_type)
            self.assertEquals(type(view4), test_img_type)

        self.assertEquals(view1.size, (44, 32))
        self.assertEquals(view2.size, (10, 19))
        self.assertEquals(view3.size, (32, 87))
        self.assertEquals(view4.size, (88, 231))

        path = 'res/gate/view'
        view1.save(f'{path}/{self.g1.tag}.png')
        view2.save(f'{path}/{self.g2.tag}.png')
        view3.save(f'{path}/{self.g3.tag}.png')
        view4.save(f'{path}/{self.g4.tag}.png')

    def test_save(self):
        pass


if __name__ == '__main__':
    unittest.main()
