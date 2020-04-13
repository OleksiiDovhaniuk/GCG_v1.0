""" Calculate fitness function value

This module contains functions for work and 
calculation the fitness function of current 
genetic algorithm.

Functions: 
    generation_result(generation, inputs, outputs, coefs),
    garbage_outs_number(inputs, outputs),
    quantum_cost(chromosome, el_quantum_cost),
    delay(chromosome, element_delay),
    elements_number(chromosome),
    err_list(chromosome, inputs, outputs), 
    fredkin_result(signals), 
    fitness_function(errors, c, g, s, coefs), 
    k_from_error(errors), g_from_c(c), h_from_g(g), i_from_s(s).

"""
import math
from timeit import timeit

FREDKIN_DELAY = 1
FREDKIN_QUANTUM_COST = 5
FREDKIN_INPUTS_NUMBER = 3
ITERATION_POWER = 100

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
    """ Calculates fitness function value. 

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

def fredkin_result(signals):
    """ Simulates Fredkin element action.

    Args: signals (list of int): list like [C_in, I1, I2].
    
    Returns: 
        [C_out, O1, O2] = [C_in, I1 XOR S, I2 XOR S],
        where S = (I1 XOR I2) AND C.

    Note:
        Input signals should be one dimensional list with 3 elements inside.

    Examples of execution:
        >>> fredkin_result([0, 0, 0])
        [0, 0, 0]
        >>> fredkin_result([0, 0, 1])
        [0, 0, 1]
        >>> fredkin_result([0, 1, 0])
        [0, 1, 0]
        >>> fredkin_result([1, 0, 0])
        [1, 0, 0]
        >>> fredkin_result([0, 1, 1])
        [0, 1, 1]
        >>> fredkin_result([1, 0, 1])
        [1, 1, 0]
        >>> fredkin_result([1, 1, 0])
        [1, 0, 1]
        >>> fredkin_result([1, 1, 1])
        [1, 1, 1]

    """
    C_out = signals[0]
    O1    = signals[2]
    O2    = signals[1]

    PQR = [C_out]
    if C_out == 1:
        PQR.append(O1)
        PQR.append(O2)
        return PQR
    else:
        return signals

def err_no(chromosome, inputs, outputs):
    """ Returns errors number of schemotechnical system.

    Args: 
        chromosome (3D list): individual one from generation.
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: err_no(int): minimal number of errors in current chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element i (n >= 0),
        m i of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [err_no(chromosome, ins_or, outs_or) \
            for chromosome in generation_or]
        [0, 0, 1, 1, 0]
        >>> [err_no(chromosome, ins_sum, outs_sum) \
            for chromosome in generation_sum]
        [0, 10, 6, 0]

    """
    ins_no = len(inputs)
    outs_no = len(outputs)

    # Copy inputs for local variable for safety of global values and switch rows <-> colums.
    inputs = list(map(list, zip(*inputs)))
    outputs = list(map(list, zip(*outputs)))

    err_no = 0
    err_list = [[0] * ins_no for _ in range(outs_no)]


    for active_ins, cheking_outs in zip(inputs, outputs):

        for gene in chromosome:
            to_switch = False 
            pos1 = pos2 = -1

            for k, gate_pos in enumerate(gene):
                if gate_pos:

                    if gate_pos == 2:
                        to_switch = bool(active_ins[k])

                        if not to_switch: 
                            break
                        
                        elif to_switch and (pos2 != -1):
                            active_ins[pos1], active_ins[pos2]\
                                = active_ins[pos2], active_ins[pos1]
                            break

                    elif pos1 == -1:
                        pos1 = k
                        
                    else:
                        pos2 = k

                        if to_switch: 
                            active_ins[pos1], active_ins[pos2]\
                                = active_ins[pos2], active_ins[pos1]
                            break

        for index in range(outs_no):
            for jndex in range(ins_no):
                err_list[index][jndex] += cheking_outs[index] ^ active_ins[jndex] 

    # calculate overall errors number
    while err_list:
        list_mins = [min(row) for row in err_list]

        err_no += min(list_mins)
        err_list.pop(list_mins.index(min(list_mins)))

    return err_no

def delay_time(chromosome, element_delay):
    """ Returns delay value of system in ns.

    Args: 
        chromosome (3D list): individual of generation.
        element_delay (float): logic gate delay in nano secunds.
    
    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> [delay_time(chromosome, 1) for chromosome in generation_or]
        [1, 1, 1, 1, 2]
        >>> [delay_time(chromosome, 3) for chromosome in generation_sum]
        [12, 12, 18, 12]

    """
    delay_list = []
    chrm = list(map(list, zip(*chromosome))) # switch rows <-> columns

    for line in chrm:
        delay_list.append(line.count(1))
        delay_list[-1] += line.count(2)

    return max(delay_list) * element_delay

def quantum_cost(chromosome, el_quantum_cost):
    """ Returns quantum value of schemotechnical system.
    
    Args: 
        chromosome (3D list): individual of generation.
        el_quantum_cost (float): logic gate quantum cost.
    
    Returns: quantum_cost (float): quantum cost of current chromosome.

    Examples of execution:
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_or]
        [5, 5, 5, 5, 10]
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_sum]
        [25, 40, 45, 35]

    """
    element_no = 0

    for gene in chromosome:
       if 2 in gene: element_no +=1
       
    return element_no * el_quantum_cost

def garbage_outs_number(signals):
    """ Returns number of garbage outputs/ extra inputs

    Args: 
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: elements_number (int): number of logic gates.

    Note: Size of inputs and outputs lists is equal. 

    Examples of execution:
        >>> garbage_outs_number([ins_or, outs_or])
        2
        >>> garbage_outs_number([ins_sum, outs_sum])
        3
    """
    align_no = 0 

    for row in signals[0]:
        if row.count(row[0]) == len(row):
            align_no += 1

    return max  (align_no, len(signals[0]) - len(signals[1]))

def generation_result(generation, inputs, outputs, coefs):
    """ Returns one dimensional list of fitness function values for current generation.

    Args: 
        generation (4D list): current generation.
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
        coefs (tuple of int): fitness function coeficients in order: α, ß, y, δ
    
    Returns: generation_result (list): fitness function values for each chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element i (n >= 0),
        m i of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [round(result, 3) for result in generation_result(generation_or, \
            ins_or, outs_or, coefs)]
        [0.978, 0.978, 0.528, 0.528, 0.963]
        >>> [round(result, 3) for result in generation_result(generation_sum, \
            ins_sum, outs_sum, coefs)]
        [0.945, 0.125, 0.169, 0.943]
    """
    results = []

    for chromosome in generation:
        e = err_no(chromosome, inputs, outputs)
        c = quantum_cost(chromosome, FREDKIN_QUANTUM_COST)
        g = garbage_outs_number([inputs, outputs])
        s = delay_time(chromosome, FREDKIN_DELAY)
         
        results.append(fitness_function(e, c, g, s, coefs))

    return results

TEST={
    'coefs': [0.9, 0.034, 0.033, 0.033],

    'ins_or': [[0, 0, 1, 1],  
               [0, 1, 0, 1],  
               [1, 1, 1, 1]],

    'outs_or': [[0, 1, 1, 1]], 

    'generation_or': [[[2, 1, 1]],
                       
                      [[0, 0, 0],
                       [1, 2, 1],
                       [0, 0, 0]],

                      [[1, 1, 2],
                       [0, 0, 0],
                       [0, 0, 0]],
                       
                      [[0, 0, 0],
                       [1, 1, 2]],
                       
                      [[0, 0, 0],
                       [1, 1, 2],
                       [0, 0, 0],
                       [2, 1, 1],
                       [0, 0, 0]]],

    'outs_sum': [[0, 1, 1, 0, 1, 0, 0, 1], 
                 [0, 0, 0, 1, 0, 1, 1, 1],
                 [0, 0, 1, 1, 1, 1, 0, 0]],

    'ins_sum': [[0, 0, 0, 0, 1, 1, 1, 1],
                [0, 0, 1, 1, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1]],

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

    # 'outs_sum': [[0, 0, 0, 2, 2, 2],
    #              [1, 0, 0, 2, 2, 2],
    #              [1, 0, 1, 2, 2, 2],
    #              [0, 1, 1, 2, 2, 2],
    #              [1, 0, 1, 2, 2, 2],
    #              [0, 1, 1, 2, 2, 2],
    #              [0, 1, 0, 2, 2, 2],
    #              [1, 1, 0, 2, 2, 2]],

    # 'ins_sum': [[0, 0, 0, 1, 0, 1],
    #             [0, 0, 1, 1, 0, 1],
    #             [0, 1, 0, 1, 0, 1],
    #             [0, 1, 1, 1, 0, 1],
    #             [1, 0, 0, 1, 0, 1],
    #             [1, 0, 1, 1, 0, 1],
    #             [1, 1, 0, 1, 0, 1],
    #             [1, 1, 1, 1, 0, 1]],

    'generation_sum': [[[0, 2, 0, 0, 1, 1],
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

def test_err_(): err_no(TEST['big_generation'][1], TEST['big_ins'], TEST['big_outs']) 

print(timeit(test_err_, number=ITERATION_POWER))

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=TEST)