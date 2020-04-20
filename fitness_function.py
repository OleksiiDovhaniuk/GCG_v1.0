""" Calculate fitness function value

This module contains functions for work and 
calculation the fitness function of current 
genetic algorithm.

Functions: 
    calculate(generation, inputs, outputs, coefs),
    garbage_outs_number(inputs, outputs),
    quantum_cost(chromosome, el_quantum_cost),
    delay_time(chromosome, element_delay),
    elements_number(chromosome),
    err_no(chromosome, sgn_no inputs, outputs), 
    fredkin_result(signals), 
    fitness_function(errors, c, g, s, coefs), 
    k_from_error(errors), g_from_c(c), h_from_g(g), i_from_s(s).

"""
import math
from timeit import timeit


FREDKIN_DELAY = 1
FREDKIN_QUANTUM_COST = 5
FREDKIN_INPUTS_NUMBER = 3
ITERATION_POWER = 300

def k_from_error(errors):
    """ Factor k based on number of errors in system.

    Args:
        errors (int): Number of errors.
    
    Returns:
        k = 1 / (errors + 1).

    Examples of execution:
        >>> [k_from_error(errors) for errors in [0, 24, 49, 99]]
        [1.0, 0.04, 0.02, 0.01]

    """
    k = 1 / (errors + 1)
    return k

def g_from_c(c):
    """ Factor g based on quantum value.

    Args: c (int): overall quantum cost value.
    
    Returns: g = exp(-( (1 - (5 / c))^2 )).

    Examples of execution:
        >>> [round(g_from_c(c), 3) for c in [5, 10, 125]]
        [1.0, 0.779, 0.398]

    """
    if c == 0:
        return 0
    else:
        x = -((1 - (FREDKIN_QUANTUM_COST / c))**2)
        g = math.exp(x)
        return g

def h_from_g(g):
    """ Factor h based on number of garbage outputs.

    Args: g (int): number of garbage outputs (extra inputs).
    
    Returns: h = 1 / (1 + g).

    Examples of execution:
        >>> [h_from_g(g) for g in [0, 24, 49, 99]]
        [1.0, 0.04, 0.02, 0.01]

    """
    h = 1 / (1 + g)
    return h

def i_from_s(s):
    """ Factor i based on value of general system delay. 

    Args: s (int): delay of circuit.
    
    Returns: i = exp(-( (1 - 1 / s)^2 )).

    Examples of execution:
        >>> [round(i_from_s(s), 3) for s in [1, 2, 25]]
        [1.0, 0.779, 0.398]

    """
    if s == 0:
        return 0
    else:
        x = -((1 - 1 / s)**2)
        i = math.exp(x)
        return i

def fitness_function(errors, c, g, s, coefs):
    """Calculates fitness function value. 

    Args: 
        errors (int): delay of circuit.
        c (int): overall quantum cost value.
        g (int): number of garbage outputs (extra inputs).
        s (int): delay of circuit.
        coefs (tuple of int): fitness function coeficients in order: α, ß, y, δ
    
    Returns: F = αK(errors) + ßG(c) + yH(g) + δI(s).

    Examples of execution:
        >>> round(fitness_function(0, 5, 0, 1, [0.7, 0.1, 0.1, 0.1]), 3)
        1.0
        >>> round(fitness_function(0, 5, 0, 1, [0.5, 0.1, 0.15, 0.25]), 3)
        1.0
        >>> round(fitness_function(24, 125, 99, 25, [0.7, 0.1, 0.1, 0.1]), 3)
        0.109

    """
    value = (coefs[0] * k_from_error(errors) + 
    coefs[1] * g_from_c(c) + 
    coefs[2] * h_from_g(g) + 
    coefs[3] * i_from_s(s))
    return value

def err_no(chromosome, sgn_no, inputs, outputs):
    """`[Warning]: description needs to be reconsidered!` 
    Returns errors number of schemotechnical system.

    Args: 
        chromosome (3D list): individual one from generation;
        sgn_no (int);
        inputs (tuple of ints): input signals from truth table,
            decimal representations of hexidicimal digits, which 
            represent `column` in the truth table;
        outputs (tuple of ints): output signals from truth table,
            decimal representations of hexidicimal digits, which 
            represent `row` in the truth table.
    
    Returns: err_no(int): minimal number of errors in current chromosome.

    Note: 
        Sizes of inputs and outputs tuples is equal. 
        Gene is look like [n (int), m (int)], 
        where n, m hexidicimal digits; n (in binar view) 
        represents positions of control gates and
        m (in binar view) represents switching gates. 

    Examples of execution:
        >>> [err_no(chromosome, no_or, ins_or, outs_or)\
            for chromosome in generation_or]
        [0, 0, 1, 1, 0]
        >>> [err_no(chromosome, no_sum, ins_sum, outs_sum) \
            for chromosome in generation_sum]
        [0, 10, 6, 0]

    """
    err_no = 0
    active_ins = inputs.copy()
    once = (2 ** sgn_no) - 1
    outs_no = len(outputs[0])
    err_list = [[0] * sgn_no for _ in range(outs_no)]

    for ins, outs in zip(active_ins, outputs): 
        for control, switch in chromosome:
            if control & ins == control:
                if '{0:b}'.format(switch & ins).count('1') == 1:
                    ins = ins ^ switch

        for sgn, errs in zip(outs, err_list):
            if sgn:
                err_segment = once ^ ins
            else:
                err_segment = ins
            segment_str = '{0:b}'.format(err_segment)[::-1]

            for i in range(sgn_no):
                try:
                    errs[-i-1] += int(segment_str[i])
                except IndexError:
                    pass

    min_list = sorted([min(row) for row in err_list])
    for min_value in min_list[:outs_no]:
        err_no += min_value

    return err_no
        
def delay_time(chromosome, sgn_no,  element_delay):
    """`[Warning]: description needs to be reconsidered!` 
    Returns delay value of system in ns.

    Args: 
        chromosome (3D list): individual of generation;
        element_delay (float): logic gate delay in nano secunds;
        sgn_no (int).

    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> [delay_time(chromosome, no_or, 1) for chromosome in generation_or]
        [1, 1, 1, 1, 2]
        >>> [delay_time(chromosome, no_sum, 3) for chromosome in generation_sum]
        [12, 15, 18, 12]

    """
    delay_list = [0] * sgn_no

    for control, switch in chromosome:
        element = '{0:b}'.format(control | switch)[::-1]
        for i in range(sgn_no):
            try:
                delay_list[i] += int(element[i])
            except IndexError:
                	pass

    return max(delay_list) * element_delay

def quantum_cost(chromosome, el_quantum_cost):
    """`[Warning]: description needs to be reconsidered!` 
    Returns quantum value of schemotechnical system.
    
    Args: 
        chromosome (3D list): individual of generation.
        el_quantum_cost (int): logic gate quantum cost.
    
    Returns: quantum_cost (int): quantum cost of current chromosome.

    Examples of execution:
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_or]
        [5, 5, 5, 5, 10]
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_sum]
        [25, 40, 45, 35]

    """
    element_no = 0

    for control, _ in chromosome:
       if control: element_no += 1
       
    return element_no * el_quantum_cost

def garbage_outs_number(sgn_no, inputs, outputs):
    """`[Warning]: description needs to be reconsidered!` 
    Returns number of garbage outputs/ extra inputs

    Args: 
        sgn_no (int): number of signals;
        inputs (tuple of ints): input signals from truth table;
        outputs (2D tuple): output signals from truth table.
    
    Returns: elements_number (int): number of logic gates.

    Note: Size of inputs and outputs lists is equal. 

    Examples of execution:
        >>> garbage_outs_number(no_or, ins_or, outs_or)
        2
        >>> garbage_outs_number(no_sum, ins_sum, outs_sum)
        3
    """
    align_no = len('{0:b}'.format(max(inputs)))

    return max(sgn_no-align_no, sgn_no-len(outputs[0]))

def calculate(generation, sgn_no, inputs, outputs, coefs):
    """ `[Warning]: description needs to be reconsidered!` 
    Returns one dimensional list of fitness function values for current generation.

    Args: 
        generation (3D list): current generation;
        sgn_no (int);
        inputs (tuple of ints): input signals from truth table;
        outputs (2D tuple): output signals from truth table;
        coefs (tuple of ints): fitness function coeficients in order: α, ß, y, δ
    
    Returns: calculate (list): fitness function values for each chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element i (n >= 0),
        m i of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [round(result, 3) for result in calculate(generation_or, no_or,\
            ins_or, outs_or, coefs)]
        [0.978, 0.978, 0.528, 0.528, 0.963]
        >>> [round(result, 3) for result in calculate(generation_sum, no_sum,\
            ins_sum, outs_sum, coefs)]
        [0.945, 0.123, 0.169, 0.943]
    """
    results = []

    for chromosome in generation:
        e = err_no(chromosome, sgn_no, inputs, outputs)
        c = quantum_cost(chromosome, FREDKIN_QUANTUM_COST)
        g = garbage_outs_number(sgn_no, inputs, outputs)
        s = delay_time(chromosome, sgn_no, FREDKIN_DELAY)
         
        results.append(fitness_function(e, c, g, s, coefs))

    return results

__values__ = {
    'coefs': [0.9, 0.034, 0.033, 0.033],
    'no_or': 3,
    'no_sum': 6,
    # 'ins_or': [[0, 0, 1, 1],  
    #            [0, 1, 0, 1],  
    #            [1, 1, 1, 1]],

    # 'outs_or': [[0, 1, 1, 1]], 

    # 'generation_or': [[[2, 1, 1]],
                       
    #                   [[0, 0, 0],
    #                    [1, 2, 1],
    #                    [0, 0, 0]],

    #                   [[1, 1, 2],
    #                    [0, 0, 0],
    #                    [0, 0, 0]],
                       
    #                   [[0, 0, 0],
    #                    [1, 1, 2]],
                       
    #                   [[0, 0, 0],
    #                    [1, 1, 2],
    #                    [0, 0, 0],
    #                    [2, 1, 1],
    #                    [0, 0, 0]]],

    'ins_or': [1, 3, 5, 7],

    'outs_or': [[0], [1], [1], [1]], 

    'generation_or':[
        [[4,3]],
                       
        [[0,0], [2,5], [0,0]],

        [[1,6], [0,0], [0,0]],
                       
        [[0,0], [1,6]],
                       
        [[0,0], [1,6], [0,0], [4,3], [0,0]]
    ],

    # 'outs_sum': [[0, 1, 1, 0, 1, 0, 0, 1], 
    #              [0, 0, 0, 1, 0, 1, 1, 1],
    #              [0, 0, 1, 1, 1, 1, 0, 0]],

    # 'ins_sum': [[0, 0, 0, 0, 1, 1, 1, 1],
    #             [0, 0, 1, 1, 0, 0, 1, 1],
    #             [0, 1, 0, 1, 0, 1, 0, 1],
    #             [1, 1, 1, 1, 1, 1, 1, 1],
    #             [0, 0, 0, 0, 0, 0, 0, 0],
    #             [1, 1, 1, 1, 1, 1, 1, 1]],

    'big_outs': [[0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1], 
                 [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
                 [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                 [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                 [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]],

    'big_ins': [[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

    'outs_sum_': [[0, 0, 0, 2, 2, 2],
                 [1, 0, 0, 2, 2, 2],
                 [1, 0, 1, 2, 2, 2],
                 [0, 1, 1, 2, 2, 2],
                 [1, 0, 1, 2, 2, 2],
                 [0, 1, 1, 2, 2, 2],
                 [0, 1, 0, 2, 2, 2],
                 [1, 1, 0, 2, 2, 2]],

    'ins_sum_': [[0, 0, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1],
                [0, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 1]],

    'generation_sum_': [[[0, 2, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [2, 1, 0, 0, 0, 1],
                        [1, 0, 0, 1, 2, 0],
                        [0, 2, 1, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 0, 2]],
                        
                       [[0, 2, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 2, 1],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 2],
                        [0, 0, 0, 0, 0, 0],
                        [0, 2, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [2, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 1],
                        [1, 0, 0, 1, 0, 2],
                        [0, 0, 0, 0, 0, 0],
                        [0, 1, 2, 0, 1, 0]],

                       [[0, 2, 1, 0, 0, 1],
                        [2, 0, 1, 0, 0, 1],
                        [2, 0, 0, 1, 1, 0],
                        [0, 1, 1, 0, 0, 2],
                        [1, 0, 0, 2, 0, 1],
                        [0, 2, 1, 0, 1, 0],
                        [1, 0, 0, 0, 1, 2],
                        [0, 2, 1, 1, 0, 0],
                        [1, 1, 0, 0, 0, 2]],

                       [[2, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 2, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [2, 0, 1, 1, 0, 0],
                        [0, 1, 0, 0, 2, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 2, 1, 0],
                        [0, 1, 1, 0, 0, 2]]],

    'ins_sum': [5, 13, 21, 29, 37, 45, 53, 61],

    # 'outs_sum': [105, 23, 60],

    # 'outs_sum': [[0, 1, 1, 0, 1, 0, 0, 1], 
    #              [0, 0, 0, 1, 0, 1, 1, 1],
    #              [0, 0, 1, 1, 1, 1, 0, 0]],

    'outs_sum': [[0, 0, 0],
                 [1, 0, 0],
                 [1, 0, 1],
                 [0, 1, 1],
                 [1, 0, 1],
                 [0, 1, 1],
                 [0, 1, 0],
                 [1, 1, 0]],

    # 'outs_sum': [0, 4, 5, 3, 5, 3, 2, 6],

    # 'outs_sum': [[0, 1, 1, 0, 1, 0, 0, 1], 
    #              [0, 0, 0, 1, 0, 1, 1, 1],
    #              [0, 0, 1, 1, 1, 1, 0, 0]],

    'generation_sum':[
        [[16, 3], [ 0, 0], [32,17], [ 2,36], [16, 9], [ 0, 0], [ 1,40]],

        [[16,12], [ 0, 0], [ 2,33], [ 0, 0], [ 1,34], [ 0, 0], [16,12], [ 0, 0], 
         [32,24], [ 0, 0], [ 8, 3], [ 1,36], [ 0, 0], [ 8,18]],

        [[16, 9], [32, 9], [32, 6], [ 1,24], [ 4,33], [16,10], [ 1,34], [16,12],
         [ 1,48]],

        [[32, 3], [ 0, 0], [ 4,24], [ 0, 0], [ 8, 3], [ 0, 0], [32,12], [ 2,17],
         [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 4,34], [ 1,24]]
    ],
    'big_generation': [[[0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 2, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 2],
                        [1, 0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 2, 0, 1],
                        [0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 2, 0, 0],
                        [2, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 2, 1, 1, 0],
                        [0, 1, 2, 0, 1, 0, 0, 0, 0]],
                       
                       [[0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 2, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 2],
                        [1, 0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 2, 0, 1],
                        [0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 2, 0, 0],
                        [2, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 2],
                        [1, 0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 2, 0, 1],
                        [0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 2, 0, 0],
                        [2, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 2],
                        [1, 0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 2, 0, 1],
                        [0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 2, 0, 0],
                        [2, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 2],
                        [1, 0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 2, 0, 1],
                        [0, 2, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 2, 0, 0],
                        [2, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 2, 1, 1, 0],
                        [0, 1, 2, 0, 1, 0, 0, 0, 0]]]
    }

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=__values__)

def test_err():
    err_no(__values__['generation_sum'][0], __values__['no_sum'], __values__['ins_sum'], __values__['outs_sum'])

print(timeit(test_err, number=ITERATION_POWER))