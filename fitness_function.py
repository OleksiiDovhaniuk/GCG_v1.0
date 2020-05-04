""" This module contains the calculation functions 
for the fitness function components and as a result 
evaluetion function for inputed generation called 
"calculate(generation, inputs, outputs, coefs)".

Functions: 
    calculate(generation, inputs, outputs, coefs),
    garbage_outs_number(inputs, outputs),
    quantum_cost(chromosome, el_quantum_cost),
    delay_time(chromosome, element_delay),
    err_no(chromosome, sgn_no inputs, outputs), 
    fitness_function(errors, c, g, s, coefs), 
    k_from_error(errors), 
    g_from_c(c), 
    h_from_g(g), 
    i_from_s(s).

"""
import math
from timeit import timeit
from copy import deepcopy


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
    return (
        coefs[0] * k_from_error(errors) + 
        coefs[1] * g_from_c(c) + 
        coefs[2] * h_from_g(g) + 
        coefs[3] * i_from_s(s)
    )

def err_no(chromosome, sgn_no, inputs, outputs):
    """Returns errors number of the scheme (or chromosome, or genotype).

    Args: 
        chromosome (3D list): one individual from the  generation;
        sgn_no (int);
        inputs (tuple of ints): input signals from truth table,
            decimal representations of hexidicimal digits, which 
            represent `column` in the truth table;
        outputs (2D tuple): output signals from truth table,
            binary representations of columns in the truth table.
    
    Returns: err_no(int): minimal number of errors in the chromosome.

    Note: 
        Gene is look like [n (int), m (int)], 
        where n, m hexidicimal digits; n (in binar view) 
        represents positions of control gates and
        m (in binar view) represents switching gates. 

    Examples of execution:
        >>> gnrtn_copy = [[[gene[0], gene[1]] for gene in chrm] for chrm in generation_or]
        >>> ins_copy = [portion for portion in ins_or]
        >>> outs_copy = [[s for s in portion] for portion in outs_or]
        >>> [err_no(chromosome, no_or, ins_or, outs_or)\
            for chromosome in generation_or]
        [0, 0, 1, 1, 0]
        >>> gnrtn_copy == generation_or
        True
        >>> [chrm_copy == chrm for chrm_copy, chrm in zip(gnrtn_copy, generation_or)]
        [True, True, True, True, True]
        >>> ins_copy == ins_or
        True
        >>> outs_copy == outs_or
        True

        >>> gnrtn_copy = [[[gene[0], gene[1]] for gene in chrm] for chrm in generation_sum]
        >>> ins_copy = [portion for portion in ins_sum]
        >>> outs_copy = [[s for s in portion] for portion in outs_sum]
        >>> [err_no(chromosome, no_sum, ins_sum, outs_sum) \
            for chromosome in generation_sum]
        [0, 10, 6, 0, 10]
        >>> gnrtn_copy == generation_sum
        True
        >>> [chrm_copy == chrm for chrm_copy, chrm in zip(gnrtn_copy, generation_sum)]
        [True, True, True, True, True]
        >>> ins_copy == ins_sum
        True
        >>> outs_copy == outs_sum
        True

        >>> [err_no(chromosome, no_sum, ins_sum, outs_sum) \
            for chromosome in test_from_res1]
        [0, 0, 0]

    """
    err_no = 0
    chromosome = [gene for gene in chromosome if gene != [0, 0]]
    out_no = len(outputs[0])
    err_list = [[0] * sgn_no for _ in range(out_no)]

    for ins, outs in zip(inputs, outputs): 
        for control, switch in chromosome:
            if control & ins == control:
                if '{0:b}'.format(switch & ins).count('1') == 1:
                    ins = ins ^ switch

        str_ins = '{0:b}'.format(ins)
        while len(str_ins) < sgn_no:
            str_ins = '0' + str_ins
            
        for i in range(len(outs)):
            for j in range(sgn_no):
                err_list[i][j] += outs[i] ^ int(str_ins[j])

    min_list = sorted([min(row) for row in err_list])
    for min_value in min_list[:out_no]:
        err_no += min_value

    return err_no
        
def delay_time(chromosome, sgn_no,  element_delay):
    """ Calculates delay value of system in units of element delay.

    Args: 
        chromosome (2D list): one individual of the generation;
        element_delay (float): logic gate delay;
        sgn_no (int).

    Returns: delay (float): delay of current chromosome.

    Examples of execution:
        >>> [delay_time(chromosome, no_or, 1) for chromosome in generation_or]
        [1, 1, 1, 1, 2]
        >>> [delay_time(chromosome, no_sum, 3) for chromosome in generation_sum]
        [12, 15, 18, 12, 18]

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
    """ Calculates quantum cost of the scheme (or chromosome, or genotype).
    
    Args: 
        chromosome (2D list): individual of generation.
        el_quantum_cost (float): logic gate quantum cost.
    
    Returns: quantum_cost (float): quantum cost of the chromosome.

    Examples of execution:
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_or]
        [5, 5, 5, 5, 10]
        >>> [quantum_cost(chromosome, 5) for chromosome in generation_sum]
        [25, 40, 45, 35, 30]

    """
    element_no = 0

    for control, _ in chromosome:
       if control: element_no += 1
       
    return element_no * el_quantum_cost

def garbage_outs_number(chromosome, sgn_no, inputs, outputs):
    """ Calculates number of garbage outputs/ extra inputs.

    Args: 
        chromosome: nested list;
        sgn_no (int): number of signals;
        inputs (tuple of ints): hexadecimal representation of
            input signals from truth table;
        outputs (2D tuple): binary representation output 
            signals from truth table.
    
    Examples of execution:
        >>> [garbage_outs_number(chrm, no_or, ins_or_complet, outs_or) for chrm in generation_or]
        [2, 2, 2, 2, 2]
        >>> [garbage_outs_number(chrm, no_sum, ins_sum_complet, outs_sum) for chrm in generation_sum]
        [3, 3, 3, 3, 0]
    """
    total_or = 0
    for control, switch in tuple(chromosome):
        total_or |= (control | switch)
    
    static_no = max(sgn_no-len(inputs), sgn_no-len(outputs[0]))
    min_no = min(sgn_no-len(inputs), sgn_no-len(outputs[0]))
    zero_no = '{0:b}'.format(total_or)[min_no:].count('0') 

    return static_no - zero_no

def calculate(generation, sgn_no, inputs_ , inputs, outputs, coefs):
    """ Calculates fitness function values for the inputed generation.

    Args: 
        generation (3D list): current generation;
        sgn_no (int);
        inputs_: dictionary;
        inputs (tuple of ints): input signals from truth table;
        outputs (2D tuple): output signals from truth table;
        coefs (tuple of ints): fitness function coeficients in order: α, ß, y, δ
    
    Returns(list of ints): evaluation values of the inputed generation.

    Examples of execution:
        >>> gnrtn_copy = deepcopy(generation_or)
        >>> gnrtn_copy == generation_or
        True
        >>> no_copy = no_or
        >>> no_copy == no_or
        True
        >>> ins_copy = deepcopy(ins_or)
        >>> ins_copy == ins_or
        True
        >>> outs_copy = deepcopy(outs_or)
        >>> outs_copy == outs_or
        True
        >>> coefs_copy = coefs.copy()
        >>> coefs_copy == coefs
        True
        >>> [round(result, 3) for result in calculate(generation_or, no_or,\
            ins_or_complet, ins_or, outs_or, coefs)]
        [0.978, 0.978, 0.528, 0.528, 0.963]
        >>> gnrtn_copy == generation_or
        True
        >>> no_copy == no_or
        True
        >>> ins_copy == ins_or
        True
        >>> ins_copy == ins_or
        True
        >>> coefs_copy == coefs
        True

        >>> gnrtn_copy = deepcopy(generation_sum)
        >>> gnrtn_copy == generation_sum
        True
        >>> no_copy = no_sum
        >>> no_copy == no_sum
        True
        >>> ins_copy = deepcopy(ins_sum)
        >>> ins_copy == ins_sum
        True
        >>> outs_copy = deepcopy(outs_sum)
        >>> outs_copy == outs_sum
        True
        >>> [round(result, 3) for result in calculate(generation_sum, no_sum,\
            ins_sum_complet, ins_sum, outs_sum, coefs)]
        [0.945, 0.123, 0.169, 0.943, 0.148]
        >>> gnrtn_copy == generation_sum
        True
        >>> no_copy == no_sum
        True
        >>> ins_copy == ins_sum
        True
        >>> outs_copy == outs_sum
        True
        >>> coefs_copy == coefs
        True

    """
    results = []

    for chromosome in generation:
        e = err_no(chromosome, sgn_no, inputs, outputs)
        c = quantum_cost(chromosome, FREDKIN_QUANTUM_COST)
        g = garbage_outs_number(chromosome, sgn_no, inputs_, outputs)
        s = delay_time(chromosome, sgn_no, FREDKIN_DELAY)
         
        results.append(fitness_function(e, c, g, s, coefs))

    return results

__test_values__ = {
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

    'ins_or_complet': {
        'X': '0011',
        'Y': '0101',
    },

    'outs_or': [[0], [1], [1], [1]], 

    'generation_or':[
        [[4,3]],
                       
        [[0,0], [2,5], [0,0]],

        [[1,6], [0,0], [0,0]],
                       
        [[0,0], [1,6]],
                       
        [[0,0], [1,6], [0,0], [4,3], [0,0]]
    ],

    'test_from_res1':[
        [[0, 0], [0, 0], [32, 6], [16, 36], [4, 10], [8, 5], [32, 3]],
        [[0, 0], [32, 6], [16, 36], [4, 10], [8, 5], [0, 0], [32, 3]],
        [[0, 0], [32, 6], [16, 36], [4, 10], [8, 5], [0, 0], [32, 3]],
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
    
    'ins_sum_complet': {
         'X': '00001111',
         'Y': '00110011',
        'C1': '01010101',
    },

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
         [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 4,34], [ 1,24]],

        [[32, 24], [16, 40], [8, 48], [0, 0], [8, 48], [16, 40], [32, 24]],
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
    doctest.testmod(extraglobs=__test_values__)


# def f1():
#     err_no(
#         __test_values__['generation_sum'][3], 
#         __test_values__['no_sum'], 
#         __test_values__['ins_sum'],
#         __test_values__['outs_sum']
#     )

# def f2():
#     err_no(
#         __test_values__['generation_sum'][3], 
#         __test_values__['no_sum'], 
#         __test_values__['ins_sum'],
#         __test_values__['outs_sum']
#     )
# n = 1000
# print(f'Without GPU: {timeit(f1, number=n)}')
# print(f'With GPU: {timeit(f2, number=n)}')
