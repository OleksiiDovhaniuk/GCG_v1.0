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
    errors_number(chromosome, inputs, outputs), 
    fredkin_result(signals), 
    fitness_function(errors, c, g, s, coefs), 
    k_from_error(errors), g_from_c(c), h_from_g(g), i_from_s(s).

"""
import math

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
    fitness_function_value = (coefs[0] * k_from_error(errors) + 
    coefs[1] * g_from_c(c) + 
    coefs[2] * h_from_g(g) + 
    coefs[3] * i_from_s(s))
    return fitness_function_value

def fredkin_result(signals):
    """ Simulates Fredkin element action.

    Args: signals (list of int): list like [A, B, C].
    
    Returns: [P, Q, R] = [A, A`B - AC, A`C - AB].

    Note:
        Input signals should be one dimensional list with 3 elements inside. 
        A` = NOT (A).

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
    A = signals[0]
    B = signals[1]
    C = signals[2]

    PQR = [A]
    if A == 1:
        PQR.append(C)
        PQR.append(B)
        return PQR
    else:
        return signals

def errors_number(chromosome, inputs, outputs):
    """ Returns errors number of schemotechnical system.

    Args: 
        chromosome (3D list): individual one from generation.
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: errors_number (int): minimal number of errors in current chromosome.

    Note: 
        Size of inputs and outputs lists is equal. 
        Number of alets is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element index (n >= 0),
        m index of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [errors_number(chromosome, ins_or, outs_or) \
            for chromosome in generation_or1]
        [0, 0, 0, 1]
        >>> [errors_number(chromosome, ins_or, outs_or) \
            for chromosome in generation_or2]
        [1, 0]
        >>> [errors_number(chromosome, ins_sum, outs_sum) \
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
                # set first signals index in path_point
                path_point[alet[1]] = alet_ind
                # set others signals in path_point
                index = alet_ind
                while sum(path_point) <= 0:
                    if gene[index][0] == alet[0]:
                        path_point[gene[index][1]] = index
                    index += 1
                signals_path.append(path_point)

    # create empty errors number list  (size = outputs number * inputs number)
    errors_number = [[0 for _ in inputs] for _ in outputs]
    # copy inputs for local variable for safetiness of global and rows <-> colums
    ins = list(map(list, zip(*inputs)))
    # copy outputs for local variable for safetiness of global and rows <-> colums
    outs = list(map(list, zip(*outputs)))
    # fill up the list 
    for row_ind, active_signals in enumerate(ins):
        # find result signals for current truth table line
        for point in signals_path:
            element_signals = [active_signals[point[i]] for i in range(len(point))]
            element_signals = fredkin_result(element_signals)
            for index, value in enumerate(point):
                active_signals[value] = element_signals[index]
        # calculate errors 
        for check_result_ind, check_result in enumerate(outs[row_ind]):
            if check_result != None:
                for result_ind, result in enumerate(active_signals):
                    if result != check_result:
                        errors_number[check_result_ind][result_ind] += 1

    # calculate overall errors number
    errors = 0
    while errors_number:
        # find min value of errors
        min = len(outs[0])
        min_ind = -1
        for row_ind, row in enumerate(errors_number):
            for value in row:
                if value < min:
                    min = value
                    min_ind = row_ind
        # add current min to overall errors value
        errors += min
        # delete row with current minimum element
        errors_number.pop(min_ind)
    return errors

def delay(chromosome, element_delay, max_delay):
    """ Returns delay value of system in ns.

    Args: 
        chromosome (3D list): individual of generation.
        element_delay (float): logic gate delay in nano secunds.
    
    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> [delay(chromosome, 1, 0) for chromosome in generation_or1]
        [1, 1, 1, 1]
        >>> [delay(chromosome, 2, 0) for chromosome in generation_or2]
        [2, 4]
        >>> [delay(chromosome, 3, 0) for chromosome in generation_sum]
        [12, 15, 18, 12]

    """
    active_colums_number = 0
    for gene in chromosome:
        for alel in gene:
            if alel != (0, 0):
                active_colums_number += 1
                break
    delay = active_colums_number * element_delay - max_delay
    if delay < 1:
        delay = 1
    return delay
        
def quantum_cost(chromosome, el_quantum_cost, max_quantum_cost):
    """ Returns quantum value of schemotechnical system.
    
    Args: 
        chromosome (3D list): individual of generation.
        el_quantum_cost (float): logic gate quantum cost.
    
    Returns: quantum_cost (float): quantum cost of current chromosome.

    Examples of execution:
        >>> [quantum_cost(chromosome, 5, 0) for chromosome in generation_or1]
        [5, 5, 5, 5]
        >>> [quantum_cost(chromosome, 5, 0) for chromosome in generation_or2]
        [5, 10]
        >>> [quantum_cost(chromosome, 5, 0) for chromosome in generation_sum]
        [25, 40, 45, 35]

    """
    elements_number = 0

    for gene in chromosome:
        check_list = [0]
        for alet in gene:
            if alet[0] not in check_list:
                check_list.append(alet[0])
                elements_number += 1

    quantum_cost = elements_number * el_quantum_cost - max_quantum_cost
    if quantum_cost < 5:
        quantum_cost = 5
    return quantum_cost

def garbage_outs_number(inputs, outputs, max_garbage_outs_number):
    """ Returns number of garbage outputs/ extra inputs

    Args: 
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: elements_number (int): number of logic gates.

    Note: Size of inputs and outputs lists is equal. 

    Examples of execution:
        >>> garbage_outs_number(ins_or, outs_or, 0)
        2
        >>> garbage_outs_number(ins_sum, outs_sum, 0)
        3
    """

    ind = 0
    for row in inputs:
        is_constant = True
        value = row[0]
        for signal in row[1:]:
            if signal != value:
                is_constant = False
                break
        if is_constant: ind += 1
    inputs_number = ind   

    ind = 0
    for row in outputs:
        is_constant = True
        value = row[0]
        for signal in row[1:]:
            if signal != value:
                is_constant = False
                break
        if is_constant: ind += 1
    outputs_number = ind    
    garbage_outs_number = max(inputs_number,outputs_number) - max_garbage_outs_number
    if garbage_outs_number < 0:
        garbage_outs_number = 0
    return garbage_outs_number

def generation_result(generation, inputs, outputs, coefs, max_delay, max_garbage_outs_number, max_quantum_cost):
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
        where n is logic element index (n >= 0),
        m index of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [round(result, 3) for result in generation_result(generation_or1, \
            ins_or, outs_or, coefs, 0, 0, 0)]
        [0.978, 0.978, 0.978, 0.528]
        >>> [round(result, 3) for result in generation_result(generation_or2, \
            ins_or, outs_or, coefs, 0, 0, 0)]
        [0.528, 0.963]
        >>> [round(result, 3) for result in generation_result(generation_sum, \
            ins_sum, outs_sum, coefs, 0, 0, 0)]
        [0.945, 0.123, 0.169, 0.943]
    """
    fitness_function_results = []
    fredkin_delay = 1
    fredkin_quantum_cost = 5

    for ind, chromosome in enumerate(generation):
        inputs_befor = inputs
        errors = errors_number(chromosome, inputs, outputs)
        inputs_after = inputs
        c = quantum_cost(chromosome, fredkin_quantum_cost, max_quantum_cost)
        g = garbage_outs_number(inputs, outputs, max_garbage_outs_number)
        s = delay(chromosome, fredkin_delay, max_delay)
        fitness_function_value = fitness_function(errors, c, g, s, coefs) 
        fitness_function_results.append(fitness_function_value)

    return fitness_function_results

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=
        {'coefs':            (0.9, 0.034, 0.033, 0.033),

         'ins_or':           [(0,0,1,1), (0,1,0,1), (1,1,1,1)],
         'outs_or':          [(0,1,1,1), (None,None,None,None), (None,None,None,None)],
         'generation_or1':    [[((1,0), (1,1), (1,2))],
                               [((1,1), (1,0), (1,2))],
                               [((1,0), (1,2), (1,1))],
                               [((1,2), (1,1), (1,0))]],
         'generation_or2':    [[((0,0), (0,0), (0,0)),
                                ((1,1), (1,2), (1,0)),
                                ((0,0), (0,0), (0,0)),
                                ((0,0), (0,0), (0,0))],
                               [((0,0), (0,0), (0,0)),
                                ((1,1), (1,2), (1,0)),
                                ((0,0), (0,0), (0,0)),
                                ((1,0), (1,2), (1,1))]],

         'ins_sum':          [(0,0,0,0,1,1,1,1), 
                                 (0,0,1,1,0,0,1,1),
                                 (0,1,0,1,0,1,0,1),
                                 (1,1,1,1,1,1,1,1),
                                 (0,0,0,0,0,0,0,0),
                                 (1,1,1,1,1,1,1,1)],
         'outs_sum':          [(0,1,1,0,1,0,0,1), 
                                 (0,0,0,1,0,1,1,1),
                                 (0,0,1,1,1,1,0,0),
                                 (None,None,None,None,None,None,None,None),
                                 (None,None,None,None,None,None,None,None),
                                 (None,None,None,None,None,None,None,None),],
         'generation_sum':   [[((0,0), (1,0), (0,0), (0,0), (1,2), (1,1)),
                                 ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                 ((1,0), (1,2), (0,0), (0,0), (0,0), (1,1)),
                                 ((2,2), (1,0), (1,1), (2,1), (2,0), (1,2)),
                                 ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                 ((1,2), (0,0), (1,1), (0,0), (0,0), (1,0))],
                              [((0,0), (1,0), (1,2), (1,1), (0,0), (0,0)),
                                 ((1,2), (0,0), (0,0), (0,0), (1,0), (1,1)),
                                 ((1,2), (2,0), (2,1), (2,2), (1,1), (1,0)),
                                 ((1,0), (1,1), (1,2), (2,0), (2,1), (2,2)),
                                 ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                 ((2,1), (1,2), (1,0), (2,2), (1,1), (2,0))],
                              [((0,0), (1,0), (1,2), (0,0), (0,0), (1,1)),
                                 ((1,0), (0,0), (1,2), (0,0), (0,0), (1,1)),
                                 ((2,0), (1,2), (1,1), (2,1), (2,2), (1,0)),
                                 ((1,2), (2,0), (2,1), (1,0), (2,2), (1,1)),
                                 ((1,2), (2,0), (2,2), (2,1), (1,1), (1,0)),
                                 ((1,1), (1,2), (0,0), (0,0), (0,0), (1,0))],
                             [((1,0), (2,1), (2,2), (2,0), (1,2), (1,1)),
                                 ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                 ((0,0), (0,0), (1,0), (0,0), (1,1), (1,2)),
                                 ((1,0), (2,1), (1,2), (1,1), (2,0), (2,2)),
                                 ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                 ((1,2), (2,1), (2,2), (1,0), (1,1), (2,0))]]
         })