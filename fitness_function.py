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
import numpy                     as np
from timeit import default_timer as timer

FREDKIN_DELAY         = 1
FREDKIN_QUANTUM_COST  = 5
FREDKIN_INPUTS_NUMBER = 3

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
        x = -((1 - (5 / c))**2)
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

def err_list(chromosome, inputs, outputs):
    """ Returns errors number of schemotechnical system.

    Args: 
        chromosome (3D list): individual one from generation.
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: err_list (int): minimal number of errors in current chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element i (n >= 0),
        m i of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [err_list(chromosome, ins_or, outs_or) \
            for chromosome in generation_or1]
        [0, 0, 0, 1]
        >>> [err_list(chromosome, ins_or, outs_or) \
            for chromosome in generation_or2]
        [1, 0]
        >>> [err_list(chromosome, ins_sum, outs_sum) \
            for chromosome in generation_sum]
        [0, 10, 6, 0]

    """
    # create list of active signals path
    signals_path = []
    # fill up the list
    for gene in chromosome:
        check_list = [0]
        for alet_ind, alet in enumerate(gene):
            if alet[0] not in check_list:
                check_list.append(alet[0])
                # create negative number of inputs for path point default values
                negative_inputs_number = -len(inputs[0])
                # empty path point list, size = 3
                path_point = [negative_inputs_number for _ in range(3)]
                # set first signals i in path_point
                path_point[alet[1]] = alet_ind
                # set others signals in path_point
                i = alet_ind
                while sum(path_point) <= 0:
                    if gene[i][0] == alet[0]:
                        path_point[gene[i][1]] = i
                    i += 1
                signals_path.append(path_point)

    # create empty errors number list  (size = outputs number * inputs number)
    err_list = [[0 for _ in inputs] for _ in outputs]
    # copy inputs for local variable for safetiness of global and rows <-> colums
    ins  = list(map(list, zip(*inputs)))
    # copy outputs for local variable for safetiness of global and rows <-> colums
    outs = list(map(list, zip(*outputs)))
    # fill up the list 
    for row_ind, active_signals in enumerate(ins):
        # find result signals for current truth table line
        for point in signals_path:
            element_signals = [active_signals[point[i]] for i in range(len(point))]
            element_signals = fredkin_result(element_signals)
            for i, value in enumerate(point):
                active_signals[value] = element_signals[i]
        # calculate errors 
        for check_result_ind, check_result in enumerate(outs[row_ind]):
            if check_result != None:
                for result_ind, result in enumerate(active_signals):
                    if result != check_result:
                        err_list[check_result_ind][result_ind] += 1

    # calculate overall errors number
    errors = 0
    while err_list:
        # find min value of errors
        min = len(outs[0])
        min_ind = -1
        for row_ind, row in enumerate(err_list):
            for value in row:
                if value < min:
                    min = value
                    min_ind = row_ind
        # add current min to overall errors value
        errors += min
        # delete row with current minimum element
        err_list.pop(min_ind)
    return errors

def err_list_(chromosome, inputs, outputs, size=10):
    """ Returns errors number of schemotechnical system.

    Args: 
        chromosome (3D list): individual one from generation.
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: err_list (int): minimal number of errors in current chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element i (n >= 0),
        m i of input on that element (0 <= m < 3). 

    Examples of execution:
        # >>> [err_list_(chromosome, ins_or, outs_or) \
        #     for chromosome in generation_or1]
        # [0, 0, 0, 1]
        # >>> [err_list_(chromosome, ins_or, outs_or) \
        #     for chromosome in generation_or2]
        # [1, 0]
        >>> [err_list_(chromosome, ins_sum, outs_sum) \
            for chromosome in generation_sum_]
        [0, 10, 6, 0]

    """
    sgn_no  = len(inputs)
    # create empty errors number list  (size = outputs number * inputs number)
    err_list = [[0 for _ in inputs] for _ in outputs]
    # copy inputs for local variable for safetiness of global and rows <-> colums
    Is  = list(map(list, zip(*inputs)))
    # copy outputs for local variable for safetiness of global and rows <-> colums
    Os  = list(map(list, zip(*outputs)))

    # chromosome = np.array([None, 2,    None, None, 1,    1,
    #                        None, None, None, None, None, None,
    #                        2,    1,    None, None, None, 1,
    #                        1,    2,    1,    None, None, None,
    #                        1,    2,    1,    None, None, None,
    #                        None, None, None, None, None, None,
    #                        None, None, None, None, None, None,
    #                        1,    None, 1,    None, None, 2,  ])

    for i, active_Is in enumerate(Is):
        j = 0
        for start_alet in chromosome[::sgn_no]:
            gate_Is = [None, None]

            for k, gate_pos in enumerate(chromosome[j: j+sgn_no]):
                if gate_pos:
                    if gate_pos == 2:
                        gate_Is[0] = active_Is[k]
                        gate_Is[1] = k
                    else:
                        gate_Is.append(active_Is[k])
                        gate_Is.append(k)

            if gate_Is[0]:
                gare_result = fredkin_result(gate_Is[::2])
                for k, index in enumerate(gate_Is[1::2]):
                    active_Is[index] = gare_result[k]

            j += sgn_no

        for check_result_ind, check_result in enumerate(Os[i]):
            if check_result:
                for result_ind, result in enumerate(active_Is):
                    if result != check_result:
                        err_list[check_result_ind][result_ind] += 1
    print(err_list)

    # calculate overall errors number
    err_no = 0
    while err_list:
        # find min value of errors
        min = len(Os[0])
        min_ind = -1
        for row_ind, row in enumerate(err_list):
            for value in row:
                if value < min:
                    min = value
                    min_ind = row_ind
        # add current min to overall errors value
        err_no += min
        # delete row with current minimum element
        err_list.pop(min_ind)

    return err_no

def delay_time(chromosome, element_delay):
    """ Returns delay value of system in ns.

    Args: 
        chromosome (3D list): individual of generation.
        element_delay (float): logic gate delay in nano secunds.
    
    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> [delay_time(chromosome, 1) for chromosome in generation_or1]
        [1, 1, 1, 1]
        >>> [delay_time(chromosome, 2) for chromosome in generation_or2]
        [2, 4]
        >>> [delay_time(chromosome, 3) for chromosome in generation_sum]
        [12, 15, 18, 12]

    """
    count = 0

    for gene in chromosome:
        for alel in gene:
            if alel != [0, 0]:
                count += 1
                break
            
    return count * element_delay

def quantum_cost(chromosome, el_quantum_cost):
    """ Returns quantum value of schemotechnical system.
    
    Args: 
        chromosome (3D list): individual of generation.
        el_quantum_cost (float): logic gate quantum cost.
    
    Returns: quantum_cost (float): quantum cost of current chromosome.

    Examples of execution:
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_or1]
        [5, 5, 5, 5]
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_or2]
        [5, 10]
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_sum]
        [25, 40, 45, 35]

    """
    elements_number = 0

    for gene in chromosome:
        elements_number +=\
            (len(gene) - gene.count([0, 0])) // FREDKIN_INPUTS_NUMBER

    return elements_number * el_quantum_cost

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
    numbers = []  

    for signal_type in signals:
        ind = 0

        for row in signal_type:
            if row.count(row[0]) == len(row):
                ind += 1

        numbers.append(ind)   

    return max(numbers[0], numbers[1])

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
        >>> [round(result, 3) for result in generation_result(generation_or1, \
            ins_or, outs_or, coefs)]
        [0.978, 0.978, 0.978, 0.528]
        >>> [round(result, 3) for result in generation_result(generation_or2, \
            ins_or, outs_or, coefs)]
        [0.528, 0.963]
        >>> [round(result, 3) for result in generation_result(generation_sum, \
            ins_sum, outs_sum, coefs)]
        [0.945, 0.123, 0.169, 0.943]
    """
    results = []

    for chromosome in generation:
        e = err_list(chromosome, inputs, outputs)
        c = quantum_cost(chromosome, FREDKIN_QUANTUM_COST)
        g = garbage_outs_number([inputs, outputs])
        s = delay_time(chromosome, FREDKIN_DELAY)
         
        results.append(fitness_function(e, c, g, s, coefs))

    return results

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=
        {'coefs':            [0.9, 0.034, 0.033, 0.033],

         'ins_or':           [[0,0,1,1], [0,1,0,1], [1,1,1,1]],
         'outs_or':          [[0,1,1,1], [None,None,None,None], [None,None,None,None]],
         'generation_or1':    [[[[1,0], [1,1], [1,2]]],
                               [[[1,1], [1,0], [1,2]]],
                               [[[1,0], [1,2], [1,1]]],
                               [[[1,2], [1,1], [1,0]]]],
         'generation_or2':    [[[[0,0], [0,0], [0,0]],
                                [[1,1], [1,2], [1,0]],
                                [[0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0]]],
                               [[[0,0], [0,0], [0,0]],
                                [[1,1], [1,2], [1,0]],
                                [[0,0], [0,0], [0,0]],
                                [[1,0], [1,2], [1,1]]]],

         'ins_sum':          [[0,0,0,0,1,1,1,1], 
                                 [0,0,1,1,0,0,1,1],
                                 [0,1,0,1,0,1,0,1],
                                 [1,1,1,1,1,1,1,1],
                                 [0,0,0,0,0,0,0,0],
                                 [1,1,1,1,1,1,1,1]],
         'outs_sum':          [[0,1,1,0,1,0,0,1], 
                                 [0,0,0,1,0,1,1,1],
                                 [0,0,1,1,1,1,0,0],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None],
                                 [None,None,None,None,None,None,None,None]],
         'generation_sum':   [[[[0,0], [1,0], [0,0], [0,0], [1,2], [1,1]],
                               [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                               [[1,0], [1,2], [0,0], [0,0], [0,0], [1,1]],
                               [[2,2], [1,0], [1,1], [2,1], [2,0], [1,2]],
                               [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                               [[1,2], [0,0], [1,1], [0,0], [0,0], [1,0]]],
                              [[[0,0], [1,0], [1,2], [1,1], [0,0], [0,0]],
                               [[1,2], [0,0], [0,0], [0,0], [1,0], [1,1]],
                               [[1,2], [2,0], [2,1], [2,2], [1,1], [1,0]],
                               [[1,0], [1,1], [1,2], [2,0], [2,1], [2,2]],
                               [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                               [[2,1], [1,2], [1,0], [2,2], [1,1], [2,0]]],
                              [[[0,0], [1,0], [1,2], [0,0], [0,0], [1,1]],
                               [[1,0], [0,0], [1,2], [0,0], [0,0], [1,1]],
                               [[2,0], [1,2], [1,1], [2,1], [2,2], [1,0]],
                               [[1,2], [2,0], [2,1], [1,0], [2,2], [1,1]],
                               [[1,2], [2,0], [2,2], [2,1], [1,1], [1,0]],
                               [[1,1], [1,2], [0,0], [0,0], [0,0], [1,0]]],
                             [[[1,0], [2,1], [2,2], [2,0], [1,2], [1,1]],
                               [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                               [[0,0], [0,0], [1,0], [0,0], [1,1], [1,2]],
                               [[1,0], [2,1], [1,2], [1,1], [2,0], [2,2]],
                               [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                               [[1,2], [2,1], [2,2], [1,0], [1,1], [2,0]]]],

        'generation_sum_': [[0, 2, 0, 0, 1, 1,
                             0, 0, 0, 0, 0, 0,
                             2, 1, 0, 0, 0, 1,
                             1, 0, 0, 1, 2, 0,
                             0, 2, 1, 0, 0, 1,
                             0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0,
                             1, 0, 1, 0, 0, 2],
                             
                            [0, 2, 1, 1, 0, 0,
                             0, 0, 0, 0, 0, 0,
                             1, 0, 0, 0, 2, 1,
                             1, 0, 0, 0, 1, 2,
                             0, 2, 1, 1, 0, 0,
                             2, 1, 1, 0, 0, 0,
                             0, 0, 0, 2, 1, 1,
                             1, 0, 0, 1, 0, 2,
                             0, 0, 0, 0, 0, 0,
                             0, 1, 2, 0, 1, 0],

                            [0, 2, 1, 0, 0, 1,
                             2, 0, 1, 0, 0, 1,
                             2, 0, 0, 1, 1, 0,
                             0, 1, 1, 0, 0, 2,
                             1, 0, 0, 2, 0, 1,
                             0, 2, 1, 0, 1, 0,
                             1, 0, 0, 0, 1, 2,
                             0, 0, 0, 0, 0, 0,
                             0, 2, 1, 1, 0, 0,
                             1, 1, 0, 0, 0, 2],

                            [2, 0, 0, 0, 1, 1,
                             0, 1, 1, 2, 0, 0,
                             0, 0, 2, 0, 1, 1,
                             0, 0, 0, 0, 0, 0,
                             2, 0, 1, 1, 0, 0,
                             0, 1, 0, 0, 2, 1,
                             0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0,
                             1, 0, 0, 2, 1, 0,
                             0, 1, 1, 0, 0, 2]]

         })

