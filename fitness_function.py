import math

fredkin_delay = 1
fredkin_quantum_cost = 5

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

def fitness_function_result(errors, c, g, s, coefs):
    """ Calculates fitness function value. 

    Args: 
        errors (int): delay of circuit.
        c (int): overall quantum cost value.
        g (int): number of garbage outputs (extra inputs).
        s (int): delay of circuit.
        coefs (tuple of int): fitness function coeficients in order: α, ß, y, δ
    
    Returns: F = αK(errors) + ßG(c) + yH(g) + δI(s).

    Examples of execution:
        >>> round(fitness_function_result(0, 5, 0, 1, [0.7, 0.1, 0.1, 0.1]), 3)
        1.0
        >>> round(fitness_function_result(0, 5, 0, 1, [0.5, 0.1, 0.15, 0.25]), 3)
        1.0
        >>> round(fitness_function_result(24, 125, 99, 25, [0.7, 0.1, 0.1, 0.1]), 3)
        0.109

    """
    f = (coefs[0] * k_from_error(errors) + 
    coefs[1] * g_from_c(c) + 
    coefs[2] * h_from_g(g) + 
    coefs[3] * i_from_s(s))
    return f

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
        Number of genes is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element index (n >= 0),
        m index of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> errors_number(chromosome_or1, ins_or, outs_or)
        0
        >>> errors_number(chromosome_or2, ins_or, outs_or)
        0
        >>> errors_number(chromosome_or3, ins_or, outs_or)
        0
        >>> errors_number(chromosome_or4, ins_or, outs_or)
        1
        >>> errors_number(chromosome_or5, ins_or, outs_or)
        1
        >>> errors_number(chromosome_or6, ins_or, outs_or)
        0
        >>> errors_number(chromosome_sum1, ins_sum, outs_sum)
        0
        >>> errors_number(chromosome_sum2, ins_sum, outs_sum)
        10
        >>> errors_number(chromosome_sum3, ins_sum, outs_sum)
        6

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
                negative_inputs_number = -len(inputs)
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
    errors_number = [[0 for _ in inputs[0]] for _ in outputs[0]]
    #copy inputs for local variable for safetiness of global
    ins = [[value for value in row] for row in inputs]
    # fill up the list
    for row_ind, active_signals in enumerate(ins):
        # find result signals for current truth table line
        for point in signals_path:
            element_signals = [active_signals[point[i]] for i in range(len(point))]
            element_signals = fredkin_result(element_signals)
            for index, value in enumerate(point):
                active_signals[value] = element_signals[index]
        # calculate errors 
        for check_result_ind, check_result in enumerate(outputs[row_ind]):
            if check_result != None:
                for result_ind, result in enumerate(active_signals):
                    if result != check_result:
                        errors_number[check_result_ind][result_ind] += 1

    # calculate overall errors number
    errors = 0
    while errors_number:
        # find min value of errors
        min = len(outputs[0])
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

def elements_number(chromosome):
    """ Returns number of elements of schemotechnical system. 

    Args: chromosome (3D list): individual one from generation.
    
    Returns: elements_number (int): number of logic elements in current chromosome.

    Examples of execution:
        >>> elements_number(chromosome_or1)
        1
        >>> elements_number(chromosome_or2)
        1
        >>> elements_number(chromosome_or3)
        1
        >>> elements_number(chromosome_or4)
        1
        >>> elements_number(chromosome_or5)
        1
        >>> elements_number(chromosome_or6)
        2
        >>> elements_number(chromosome_sum1)
        5
        >>> elements_number(chromosome_sum2)
        8
        >>> elements_number(chromosome_sum3)
        9

    """
    elements_number = 0

    for gene in chromosome:
        check_list = [0]
        for alet in gene:
            if alet[0] not in check_list:
                check_list.append(alet[0])
                elements_number += 1

    return elements_number

def delay(chromosome, element_delay):
    """ Returns delay value of system in ns.

    Args: 
        chromosome (3D list): individual of generation.
        element_delay (float): logic gate delay in nano secunds.
    
    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> delay(chromosome_or1, 5)
        5
        >>> delay(chromosome_or2, 5)
        5
        >>> delay(chromosome_or3, 2)
        2
        >>> delay(chromosome_or4, 10)
        10
        >>> delay(chromosome_or5, 3)
        3
        >>> delay(chromosome_or6, 2)
        4
        >>> delay(chromosome_sum1, 1)
        5
        >>> delay(chromosome_sum2, 2)
        16
        >>> delay(chromosome_sum3, 3)
        27

    """
    return elements_number(chromosome) * element_delay
        
def quantum_cost(chromosome, el_quantum_cost):
    """ Returns quantum value of schemotechnical system.
    
    Args: 
        chromosome (3D list): individual of generation.
        el_quantum_cost (float): logic gate quantum cost.
    
    Returns: quantum_cost (float): quantum cost of current chromosome.

    Examples of execution:
        >>> quantum_cost(chromosome_or1, 5)
        5
        >>> quantum_cost(chromosome_or2, 5)
        5
        >>> quantum_cost(chromosome_or3, 2)
        2
        >>> quantum_cost(chromosome_or4, 10)
        10
        >>> quantum_cost(chromosome_or5, 3)
        3
        >>> quantum_cost(chromosome_or6, 2)
        4
        >>> quantum_cost(chromosome_sum1, 1)
        5
        >>> quantum_cost(chromosome_sum2, 2)
        16
        >>> quantum_cost(chromosome_sum3, 3)
        27

    """
    return elements_number(chromosome) * el_quantum_cost


def garbage_outs_number(inputs, outputs):
    """ Returns number of garbage outputs/ extra inputs

    Args: 
        inputs (2D tuple): input signals from truth table.
        outputs (2D tuple): output signals from truth table.
    
    Returns: elements_number (int): number of logic gates.

    Note: Size of inputs and outputs lists is equal. 

    Examples of execution:
        >>> garbage_outs_number(ins_or[0], outs_or[0])
        2
        >>> garbage_outs_number(ins_sum[0], outs_sum[0])
        3
    """

    ind = 0
    for signal_value in inputs:
        if signal_value == None:
            break
        ind += 1
    inputs_number = ind    

    ind = 0
    for signal_value in outputs:
        if signal_value == None:
            break
        ind += 1
    outputs_number = ind    
    return abs(inputs_number - outputs_number)

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
        Number of genes is equal to number of rows in inputs/outputs list.
        Alet is look like [n (int), m (int)], 
        where n is logic element index (n >= 0),
        m index of input on that element (0 <= m < 3). 

    Examples of execution:
        >>> [round(result, 3) for result in generation_result([chromosome_or1, \
            chromosome_or2, chromosome_or3, chromosome_or4], ins_or, outs_or, coefs)]
        [0.978, 0.978, 0.978, 0.528]
        >>> [round(result, 3) for result in generation_result([chromosome_sum1, \
            chromosome_sum2, chromosome_sum3], ins_sum, outs_sum, coefs)]
        [0.944, 0.121, 0.167]
    """
    fitness_function_results = []

    for ind, chromosome in enumerate(generation):
        inputs_befor = inputs
        errors = errors_number(chromosome, inputs, outputs)
        inputs_after = inputs
        c = quantum_cost(chromosome, fredkin_quantum_cost)
        g = garbage_outs_number(inputs[0], outputs[0])
        s = delay(chromosome, fredkin_delay)
        fitness_function_value = fitness_function_result(errors, c, g, s, coefs) 
        fitness_function_results.append(fitness_function_value)

    return fitness_function_results

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'coefs':            (0.9, 0.034, 0.033, 0.033),

                                'ins_or':           [(0,0,1), (0,1,1), (1,0,1), (1,1,1)],
                                'outs_or':          [(0, None, None), (1, None, None), (1, None, None), (1, None, None)],
                                'chromosome_or1':   [((1,0), (1,1), (1,2))],
                                'chromosome_or2':   [((1,1), (1,0), (1,2))],
                                'chromosome_or3':   [((1,0), (1,2), (1,1))],
                                'chromosome_or4':   [((1,2), (1,1), (1,0))],
                                'chromosome_or5':   [((0,0), (0,0), (0,0)),
                                                     ((1,1), (1,2), (1,0)),
                                                     ((0,0), (0,0), (0,0)),
                                                     ((0,0), (0,0), (0,0))],
                                'chromosome_or6':   [((0,0), (0,0), (0,0)),
                                                     ((1,1), (1,2), (1,0)),
                                                     ((0,0), (0,0), (0,0)),
                                                     ((1,0), (1,2), (1,1))],

                                'ins_sum':          [(0,0,0,1,0,1), 
                                                     (0,0,1,1,0,1),
                                                     (0,1,0,1,0,1),
                                                     (0,1,1,1,0,1),
                                                     (1,0,0,1,0,1),
                                                     (1,0,1,1,0,1),
                                                     (1,1,0,1,0,1),
                                                     (1,1,1,1,0,1)],
                                'outs_sum':         [(0,0,0,None,None,None),
                                                     (1,0,0,None,None,None),
                                                     (1,0,1,None,None,None),
                                                     (0,1,1,None,None,None),
                                                     (1,0,1,None,None,None),
                                                     (0,1,1,None,None,None),
                                                     (0,1,0,None,None,None),
                                                     (1,1,0,None,None,None)],
                                'chromosome_sum1':  [((0,0), (1,0), (0,0), (0,0), (1,2), (1,1)),
                                                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                                     ((1,0), (1,2), (0,0), (0,0), (0,0), (1,1)),
                                                     ((2,2), (1,0), (1,1), (2,1), (2,0), (1,2)),
                                                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                                     ((1,2), (0,0), (1,1), (0,0), (0,0), (1,0))],
                                'chromosome_sum2':  [((0,0), (1,0), (1,2), (1,1), (0,0), (0,0)),
                                                     ((1,2), (0,0), (0,0), (0,0), (1,0), (1,1)),
                                                     ((1,2), (2,0), (2,1), (2,2), (1,1), (1,0)),
                                                     ((1,0), (1,1), (1,2), (2,0), (2,1), (2,2)),
                                                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
                                                     ((2,1), (1,2), (1,0), (2,2), (1,1), (2,0))],
                                'chromosome_sum3':  [((0,0), (1,0), (1,2), (0,0), (0,0), (1,1)),
                                                     ((1,0), (0,0), (1,2), (0,0), (0,0), (1,1)),
                                                     ((2,0), (1,2), (1,1), (2,1), (2,2), (1,0)),
                                                     ((1,2), (2,0), (2,1), (1,0), (2,2), (1,1)),
                                                     ((1,2), (2,0), (2,2), (2,1), (1,1), (1,0)),
                                                     ((1,1), (1,2), (0,0), (0,0), (0,0), (1,0))]
                                })
