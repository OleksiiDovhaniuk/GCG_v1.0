""" The module is designed to test the fitness_functoin module.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Update: 15.01.2021

"""


from component.node import Node
from component.gate import Gate
from calc import fitness_function as ff
from copy import deepcopy
import numpy as np
import unittest
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')


class TestFitnessFunction(unittest.TestCase):

    def setUp(self):
        empty = [Gate(
            tag='None',
            qcost=0,
            delay=0,
            nodes={'None': Node('__dot_white_triangle_down')},
            mapping=[[0], [1]]),
            []]
        CNOT_NODES = {
            'Control': Node('__circle_black'),
            'Not': Node('__circle_crossed'),
        }
        CNOT = Gate('CNOT', 2, 1, CNOT_NODES, [[0, 0], [1, 1], [0, 1], [1, 0]])
        FRG_NODES = {
            'Control': Node('__circle_black'),
            'Target1': Node('__cross'),
            'Target2': Node('__cross')
        }
        FRG = Gate('FRG', 5, 5, FRG_NODES, [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 0, 1],
            [0, 0, 1],
            [1, 1, 0],
            [0, 1, 1],
            [1, 1, 1]
        ])
        NOT2C_NODES = {'Not': Node('__circle_crossed')}
        NOT = Gate('NOT', 2, 1.25, NOT2C_NODES, [[1], [0]])
        NOT2C_NODES = {
            'Control1': Node('__circle_black'),
            'Control2': Node('__circle_black'),
            'Not': Node('__circle_crossed'),
        }
        NOT2C = Gate('NOT2C', 4, 6.75, NOT2C_NODES, [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 0],
        ])
        self.RND = 3  # INT value for rounding results.

        # OR scheme constants.
        self.INS_OR = np.array(
            [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]], copy=False)
        self.OUTS_OR = np.array([[0], [1], [1], [1]], copy=False)
        self.QCOST_OR = [5, 5, 5, 5, 5, 2, 2, 2]
        self.DELAY_OR = [5, 5, 5, 5, 5, 1, 1, 1.25]
        self.G_OR = [
            [[FRG, [2, 1, 0]]],  # 0
            [empty, [FRG, [1, 0, 2]], empty],  # 1
            [[FRG, [0, 1, 2]], empty, empty],  # 2
            [empty, [FRG, [0, 1, 2]]],  # 3
            [empty, [FRG, [0, 1, 2]], empty, [FRG, [2, 0, 1]], empty],  # 4
            [empty, [CNOT, [1, 0]], [FRG, [1, 0, 2]]],  # 5
            [[CNOT, [1, 0]], [FRG, [1, 0, 2]], [CNOT, [0, 1]], [CNOT, [0, 2]]],  # 6
            [[NOT, [0]], [NOT, [1]], [NOT2C, [0, 1, 2]]]  # 7
        ]
        self.RES_OR = [
            np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1],
                      [1, 1, 1]], copy=False),  # 0
            np.array([[0, 0, 1], [1, 1, 0], [1, 0, 1],
                      [1, 1, 1]], copy=False),  # 1
            np.array([[0, 0, 1], [0, 1, 1], [1, 1, 0],
                      [1, 1, 1]], copy=False),  # 2
            np.array([[0, 0, 1], [0, 1, 1], [1, 1, 0],
                      [1, 1, 1]], copy=False),  # 3
            np.array([[0, 0, 1], [1, 0, 1], [1, 1, 0],
                      [1, 1, 1]], copy=False),  # 4
            np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1],
                      [1, 1, 0]], copy=False),  # 5
            np.array([[0, 0, 1], [1, 0, 0], [1, 1, 0],
                      [1, 0, 1]], copy=False),  # 6
            np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1],
                      [0, 0, 1]], copy=False),  # 7
        ]

        # AND scheme constants.
        self.INS_ADD = np.array([
            [0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 0, 1],
            [0, 1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 1]], copy=False)
        self.OUTS_ADD = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 1],
            [0, 1, 0],
            [1, 1, 0]], copy=False)
        self.G_ADD = [
            # 0
            [[FRG, [4, 0, 1]], empty, [FRG, [5, 0, 4]], [FRG, [1, 2, 5]],
             [FRG, [4, 0, 3]], empty, [FRG, [0, 3, 5]]],
            # 1
            [[FRG, [4, 2, 3]], empty, [FRG, [1, 0, 5]], empty,
             [FRG, [0, 2, 5]], empty, [FRG, [4, 3, 2]], empty,
             [FRG, [5, 4, 3]], empty, [FRG, [3, 0, 1]], [FRG, [0, 2, 5]],
             empty, [FRG, [3, 4, 1]]],
            # 2
            [[FRG, [4, 0, 3]], [FRG, [5, 3, 0]], [FRG, [5, 1, 2]], [FRG, [0, 3, 4]],
             [FRG, [2, 0, 5]], [FRG, [4, 1, 3]], [
                 FRG, [0, 1, 5]], [FRG, [4, 2, 3]],
             [FRG, [0, 4, 5]]],
            # 3
            [[FRG, [5, 3, 4]], empty, [FRG, [2, 3, 4]], empty,
             [FRG, [3, 0, 1]], empty, [FRG, [5, 2, 1]], [FRG, [1, 0, 4]],
             empty, empty, empty, empty,
             empty, [FRG, [2, 1, 5]], [FRG, [0, 3, 4]]],
            # 4
            [[FRG, [5, 3, 4]], [FRG, [4, 3, 5]], [FRG, [3, 4, 5]], empty,
             [FRG, [3, 4, 5]], [FRG, [4, 3, 5]], [FRG, [5, 3, 4]]],
            # 5
            [empty, empty, [FRG, [5, 1, 2]], [FRG, [4, 2, 5]],
             [FRG, [2, 1, 3]], [FRG, [3, 0, 2]], [FRG, [5, 0, 1]]],
            # 6
            [empty, [FRG, [5, 1, 2]], [FRG, [4, 2, 5]], [FRG, [2, 1, 3]],
             [FRG, [3, 0, 2]], empty, [FRG, [5, 0, 1]]],
            # 7
            [[FRG, [1, 4, 5]], [FRG, [0, 1, 5]], [FRG, [4, 3, 0]],
                [FRG, [1, 2, 5]], [FRG, [5, 2, 0]]],
            # 8
            [[FRG, [0, 4, 5]], [FRG, [1, 4, 5]], [FRG, [0, 1, 3]],
                [FRG, [4, 2, 5]], [FRG, [5, 1, 2]]],
        ]
        self.RES_ADD = [
            # 0
            np.array([
                [0, 0, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 1],
                [0, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 0],
                [1, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 0],
                [1, 1, 1, 1, 1, 0]], copy=False),
            # 1
            np.array([
                [0, 0, 0, 0, 1, 1],
                [0, 0, 1, 0, 1, 1],
                [1, 0, 0, 1, 1, 0],
                [1, 1, 1, 0, 1, 0],
                [0, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 1],
                [1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 1]], copy=False),
            # 2
            np.array([
                [1, 1, 0, 0, 0, 0],
                [1, 1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 0, 1, 0],
                [1, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 0, 1],
                [1, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 1]], copy=False),
            # 3
            np.array([
                [0, 0, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 1, 1],
                [1, 0, 0, 1, 0, 1],
                [0, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1]], copy=False),
            # 4
            np.array([
                [0, 0, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1],
                [0, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 1]], copy=False),
            # 5
            np.array([
                [0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1],
                [1, 1, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 1]], copy=False),
            # 6
            np.array([
                [0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1],
                [1, 1, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 1]], copy=False),
            # 7
            np.array([
                [0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 1],
                [1, 1, 0, 0, 1, 0],
                [0, 1, 1, 0, 1, 1],
                [1, 1, 0, 1, 0, 0],
                [0, 1, 1, 1, 0, 1],
                [0, 0, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 1]
            ]),
            # 8
            np.array([
                [0, 0, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 1, 0],
                [0, 0, 1, 1, 1, 1],
                [1, 1, 0, 0, 1, 0],
                [1, 0, 1, 0, 1, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 0, 1]
            ]),
        ]

    def tearDown(self):
        """ The function is called after each test function is executed.

        If there are connections are needed to enject, 
        then enter appropriate code below.

        """
        pass

    def test_calc(self):
        # Default calc settings.
        coefs_or = [.45, .45, .034, .033, .033]
        coefs_add = [.41, .41, .06, .06, .06]
        res_or = [round(ff.calc(chrm, self.INS_OR, self.OUTS_OR, coefs_or, q, d, False)['Fitness function'], self.RND)
                  for chrm, q, d in zip(self.G_OR, self.QCOST_OR, self.DELAY_OR)]
        res_add = [round(ff.calc(chrm, self.INS_ADD, self.OUTS_ADD, coefs_add, 5, 5, False)['Fitness function'], self.RND)
                   for chrm in self.G_ADD]
        self.assertEqual(
            res_or, [.753, .978, .978, .978, .963, .648, .644, .609])
        self.assertEqual(
            res_add, [.532, .534, .528, .521, .567, .534, .534, .901, .901])

        # Calculate only ordered outputs positively.
        coefs_or = [.45, .45, .034, .033, .033]
        coefs_add = [.41, .41, .06, .06, .06]
        res_or = [round(ff.calc(chrm, self.INS_OR, self.OUTS_OR, coefs_or, q, d)['Fitness function'], self.RND)
                  for chrm, q, d in zip(self.G_OR, self.QCOST_OR, self.DELAY_OR)]
        res_add = [round(ff.calc(chrm, self.INS_ADD, self.OUTS_ADD, coefs_add, 5, 5)['Fitness function'], self.RND)
                   for chrm in self.G_ADD]
        self.assertEqual(
            res_or, [.753, .978, .753, .753, .963, .648, .644, .272])
        self.assertEqual(
            res_add, [.528, .52, .519, .521, .567, .534, .534, .536, .518])

    def test_error_coef(self):
        res = [ff.error_coef(error) for error in [0, 24, 49, 99]]
        self.assertEqual(res, [1, 0.04, 0.02, 0.01])

    def test_parity_coef(self):
        res = [round(ff.parity_coef(value), self.RND)
               for value in (0, 1, 2, 99, 1000, 345)]
        self.assertEqual(res, [1, .5, .333, 0.01, 0.001, 0.003])

    def test_qcost_coef(self):
        res1 = [round(ff.qcost_coef(value, 5), self.RND)
                for value in (0, 5, 10, 125)]
        res2 = [round(ff.qcost_coef(value, 3), self.RND)
                for value in (0, 3, 10, 125)]
        res3 = [ff.qcost_coef(value, value) for value in (1, 2, 4, 6)]
        res4 = [ff.qcost_coef(0, min_values) for min_values in (1, 2, 4, 6)]
        self.assertEqual(res1, [0, 1, 0.779, 0.398])
        self.assertEqual(res2, [0, 1, 0.613, 0.386])
        self.assertEqual(res3, [1, 1, 1, 1])
        self.assertEqual(res4, [0, 0, 0, 0])

    def test_garbage_output_coef(self):
        res = [ff.error_coef(value) for value in [0, 4, 9, 999]]
        self.assertEqual(res, [1.0, 0.2, 0.1, 0.001])

    def test_delay_coef(self):
        res1 = [round(ff.delay_coef(value, 1), self.RND)
                for value in (0, 1, 2, 25)]
        res2 = [round(ff.delay_coef(value, 2), self.RND)
                for value in (0, 2, 9, 49)]
        res3 = [ff.delay_coef(value, value) for value in (3, 4, 5, 6)]
        self.assertEqual(res1, [0, 1, 0.779, 0.398])
        self.assertEqual(res2, [0, 1, 0.546, 0.399])
        self.assertEqual(res3, [1, 1, 1, 1])

    def test_err_no(self):
        res_or = [ff.err_no(res, self.OUTS_OR) for res in self.RES_OR]
        res_add = [ff.err_no(res, self.OUTS_ADD) for res in self.RES_ADD]
        self.assertEqual(res_or, [1, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(res_add, [9, 7, 8, 10, 10, 8, 8, 0, 0])

    def test_err_no_ordered(self):
        res_or = [ff.err_no_ordered(res, self.OUTS_OR) for res in self.RES_OR]
        res_add = [ff.err_no_ordered(res, self.OUTS_ADD)
                   for res in self.RES_ADD]
        self.assertEqual(res_or, [1, 0, 1, 1, 0, 0, 0, 3])
        self.assertEqual(res_add, [10, 10, 10, 10, 10, 8, 8, 8, 14])

    def test_disparity(self):
        res_or = [ff.disparity(res, self.INS_OR) for res in self.RES_OR]
        res_add = [ff.disparity(res, self.INS_ADD) for res in self.RES_ADD]
        self.assertEqual(res_or, [0, 0, 0, 0, 0, 2, 2, 3])
        self.assertEqual(res_add, [0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_qcost(self):
        res_or = [ff.qcost(chrm) for chrm in self.G_OR]
        res_add = [ff.qcost(chrm) for chrm in self.G_ADD]
        self.assertEqual(res_or, [5, 5, 5, 5, 10, 7, 11, 8])
        self.assertEqual(res_add, [25, 40, 45, 35, 30, 25, 25, 25, 25])

    def test_garbage_output(self):
        res_or = [ff.garbage_output(chrm, self.INS_OR, self.OUTS_OR)
                  for chrm in self.G_OR]
        res_add = [ff.garbage_output(
            chrm, self.INS_ADD, self.OUTS_ADD) for chrm in self.G_ADD]
        self.assertEqual(res_or, [2, 2, 2, 2, 2, 2, 2, 2])
        self.assertEqual(res_add, [3, 3, 3, 3, 0, 3, 3, 3, 3])

    def test_delay(self):
        res_or = [round(ff.delay(chrm), self.RND) for chrm in self.G_OR]
        res_add = [round(ff.delay(chrm), self.RND) for chrm in self.G_ADD]
        self.assertEqual(res_or, [5, 5, 5, 5, 10, 6, 8, 8])
        self.assertEqual(res_add, [20, 30, 30, 30, 30, 25, 25, 20, 20])

    def test_res_sgn(self):
        res_or = [np.all(ff.res_sgn(chrm, self.INS_OR) == res)
                  for chrm, res in zip(self.G_OR, self.RES_OR)]
        res_add = [np.all(ff.res_sgn(chrm, self.INS_ADD) == res)
                   for chrm, res in zip(self.G_ADD, self.RES_ADD)]

        self.assertEqual(
            res_or, [True, True, True, True, True, True, True, True])
        self.assertEqual(res_add, [True, True, True,
                                   True, True, True, True, True, True])


if __name__ == '__main__':
    unittest.main()
