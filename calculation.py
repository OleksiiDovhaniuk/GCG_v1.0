import math

fredkin_delay = 1
fredkin_quantum_cost = 5

def k_from_error(errors):
    """ Factor k based on number of errors in system. Return k = 1 / (errors + 1).

    Examples of execution:
    >>> k_from_error(0)
    1.0
    >>> k_from_error(24)
    0.04
    >>> k_from_error(49)
    0.02
    >>> k_from_error(99)
    0.01
    """
    k = 1 / (errors + 1)
    return k

def g_from_c(c):
    """ Factor g based on quantum value. Return g = exp(-((1 - (5 / c))^2)).

    Examples of execution:
    >>> g_from_c(5)
    1.0
    >>> g_from_c(10)
    0.7788007830714049
    >>> g_from_c(125)
    0.3978819204512047
    """
    if c == 0:
        return 0
    else:
        x = -((1 - (5 / c))**2)
        g = math.exp(x)
        return g

def h_from_g(g):
    """ Factor h based on number of garbage outputs. Return h = 1 / (1 + g).

    Examples of execution:
    >>> h_from_g(0)
    1.0
    >>> h_from_g(24)
    0.04
    >>> h_from_g(49)
    0.02
    >>> h_from_g(99)
    0.01
    """
    h = 1 / (1 + g)
    return h

def i_from_s(s):
    """ Factor i based on value of general system delay. Return i = exp(-((1 - 1 / s)^2)).

    Examples of execution:
    >>> i_from_s(1)
    1.0
    >>> i_from_s(2)
    0.7788007830714049
    >>> i_from_s(25)
    0.3978819204512047
    """
    if s == 0:
        return 0
    else:
        x = -((1 - 1 / s)**2)
        i = math.exp(x)
        return i

def fitness_function_result(errors, c, g, s, coefs):
    """ Return F = αK(errors) + ßG(c) + yH(g) + δI(s).

    coefs is a list of fitness function coeficients relative to order: α, ß, y, δ

    Examples of execution:
    >>> round(fitness_function_result(0, 5, 0, 1, [0.7, 0.1, 0.1, 0.1]), 5)
    1.0
    >>> round(fitness_function_result(0, 5, 0, 1, [0.5, 0.1, 0.15, 0.25]), 5)
    1.0
    >>> round(fitness_function_result(24, 125, 99, 25, [0.7, 0.1, 0.1, 0.1]), 5)
    0.10858
    """
    f = (coefs[0] * k_from_error(errors) + 
    coefs[1] * g_from_c(c) + 
    coefs[2] * h_from_g(g) + 
    coefs[3] * i_from_s(s))
    return f

def fredkin_result(signals):
    """Return list from (A, B, C) => (P, Q, R) = (A, A`B - AC, A`C - AB).
    Input signals should be one dimensional list with 3 elements inside 

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
    """ Return errors number of schemotechnical system.

    Examples of execution:
    >>> errors_number(gene_test10, ins_test10, outs_test10)
    0
    >>> errors_number(gene_test11, ins_test10, outs_test10)
    0
    >>> errors_number(gene_test12, ins_test10, outs_test10)
    0
    """
    for row in inputs:
        print(row)
    print()
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
    # fill up the list
    for row_ind, active_signals in enumerate(inputs):
        # find result signals for current truth table line
        for point in signals_path:
            element_signals = [active_signals[point[i]] for i in range(len(point))]
            element_signals = fredkin_result(element_signals)
            for index, value in enumerate(point):
                active_signals[value] = element_signals[index]
        # calculate errors 
        for check_result_ind, check_result in enumerate(outputs[row_ind]):
            for result_ind, result in enumerate(active_signals):
                if result != check_result:
                    errors_number[check_result_ind][result_ind] += 1

    # for row in errors_number:
    #     print(row)
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
    """ Return number of elements of schemotechnical system. 

    Examples of execution:
    >>> elements_number(gene_test1)
    1
    >>> elements_number(gene_test2)
    3
    >>> elements_number(gene_test3)
    0
    >>> elements_number(gene_test4)
    18
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
    """ Return delay value of system in ns.

    Examples of execution:
    >>> delay(gene_test1, 1)
    1
    >>> delay(gene_test2, 1)
    3
    >>> delay(gene_test1, 2)
    2
    >>> delay(gene_test2, 2)
    6
    """
    return elements_number(chromosome) * element_delay
        
def quantum_cost(chromosome, el_quantom_cost):
    """ Return quantum value of schemotechnical system. 

    Examples of execution:
    >>> quantum_cost(gene_test1, 5)
    5
    >>> quantum_cost(gene_test2, 5)
    15
    >>> quantum_cost(gene_test1, 2)
    2
    >>> quantum_cost(gene_test2, 2)
    6
    """
    return elements_number(chromosome) * el_quantom_cost


def garbage_outs_number(inputs_number, outputs_number):
    """ Return number of garbage outputs/ extra inputs

    Examples of execution:
    >>> garbage_outs_number(3, 5)
    2
    >>> garbage_outs_number(2, 2)
    0
    """
    return abs(inputs_number - outputs_number)

def generation_result(generation, inputs, outputs, coefs):
    """ Returns one dimensional list of fitness function values for current generation.

    Generation is 4d list, input and output signals should be 2d lists, 
    *args are one dimensional list with fitness function coeficients 
    in order: alphe, betta, gamma, delta.  

    Examples of execution:
    >>> round(generation_result([gene_test10, gene_test10, gene_test10], ins_test10, outs_test10, coefs_test1)[0], 3)
    0.944
    >>> round(generation_result([gene_test10], ins_test10, outs_test10, coefs_test1)[0], 3)
    0.944
    >>> round(generation_result([gene_test11], ins_test10, outs_test10, coefs_test1)[0], 3)
    0.944
    >>> round(generation_result([gene_test12], ins_test10, outs_test10, coefs_test1)[0], 3)
    0.944
    """
    fitness_function_results = []

    for ind, chromosome in enumerate(generation):
        inputs_befor = inputs
        errors = errors_number(chromosome, inputs, outputs)
        inputs_after = inputs
        c = quantum_cost(chromosome, fredkin_quantum_cost)
        g = garbage_outs_number(len(inputs[0]), len(outputs[0]))
        s = delay(chromosome, fredkin_delay)
        fitness_function_value = fitness_function_result(errors, c, g, s, coefs) 
        fitness_function_results.append(fitness_function_value)

    return fitness_function_results

# def test_local_variable(my_list):

#     for x in my_list:
#         x += 10
#     return my_list

# my_list = [0,1,2,3,4,5]
# print(test_local_variable(my_list))
# print(my_list)
# inputs = [[0,0,0,0],[1,1,1,1],[2,2,2,2]]
# errors_number = [[0 for _ in inputs[0]] for _ in inputs[0]]
# errors_number[2] = [1,1,0,1]

print(errors_number)

def test_outer(list):
    for i in range(3):
        test_inner(list)
    return list

def test_inner(list):
    print(list)
    for x in list:
        x += 10

print(test_outer([1,2,3,4,5]))

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod(extraglobs={'coefs_test1':  [0.9, 0.034, 0.033, 0.033],
#                                 'gene_test1':   [[[1,0], [1,1], [1,2]]],
#                                 'gene_test2':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]]],
#                                 'gene_test3':   [[[0,0], [0,0], [0,0]], [[0,0], [0,0], [0,0]]],
#                                 'gene_test4':   [[[1,0], [2,0], [3,0]], [[1,0], [3,0], [2,0]], \
#                                                  [[2,0], [1,0], [3,0]], [[2,0], [3,0], [1,0]], \
#                                                  [[3,0], [1,0], [2,0]], [[3,0], [2,0], [1,0]]],
#                                 'gene_test5':   [[[1,1], [0,0]], [[1,0], [0,0]]],
#                                 'gene_test6':   [[[1,1]], [[0,0]]],
#                                 'gene_test7':   [[[1,0], [0,0]], [[1,2], [0,0]]],
#                                 'gene_test8':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]], \
#                                                  [[2,1], [2,2], [0,0]], [[3,0], [3,1], [3,2]]],
#                                 'gene_test9':   [[[1,0], [1,1], [1,2], [2,0], [2,1], [2,2]], \
#                                                  [[0, 0], [0, 0], [1,1], [1,0], [1,2], [0, 0]]],
#                                 'gene_test10':  [[[0,0], [1,0], [0,0], [0,0], [1,2], [1,1]],
#                                                  [[1,0], [1,2], [0,0], [0,0], [0,0], [1,1]], \
#                                                  [[2,2], [1,0], [1,1], [2,1], [2,0], [1,2]], \
#                                                  [[1,2], [0,0], [1,1], [0,0], [0,0], [1,0]]],
#                                 'gene_test11':  [[[0,0], [1,0], [1,2], [1,1], [0,0], [0,0]], \
#                                                  [[1,2], [0,0], [0,0], [0,0], [1,0], [1,1]], \
#                                                  [[1,2], [2,0], [2,1], [2,2], [1,1], [1,0]], \
#                                                  [[1,0], [1,1], [1,2], [2,0], [2,1], [2,2]], \
#                                                  [[2,1], [1,2], [1,0], [2,2], [1,1], [2,0]]],
#                                 'gene_test12':  [[[0,0], [1,0], [1,2], [0,0], [0,0], [1,1]], \
#                                                  [[1,0], [0,0], [1,2], [0,0], [0,0], [1,1]], \
#                                                  [[2,0], [1,2], [1,1], [2,1], [2,2], [1,0]], \
#                                                  [[1,2], [2,0], [2,1], [1,0], [2,2], [1,1]], \
#                                                  [[1,2], [2,0], [2,2], [2,1], [1,1], [1,0]], \
#                                                  [[1,1], [1,2], [0,0], [0,0], [0,0], [1,0]]],
#                                 'ins2_1_test1': [[0,0,0], [0,1,0], [1,0,0], [1,1,0]],
#                                 'ins2_1_test2': [[0,0,1], [0,1,1], [1,0,1], [1,1,1]],
#                                 'insInv_test5': [[0, 1], [1, 1]],
#                                 'insInv_test6': [[0], [1]],
#                                 'insInv_test7': [[0, 1], [0, 0]],
#                                 'ins_test9':    [[0,0,0,0,1,0], [0,0,0,1,1,0], [0,0,1,0,1,0], [0,0,1,1,1,0]],

#                                 'ins_test10':   [[0,0,0,1,0,1], [0,0,1,1,0,1], [0,1,0,1,0,1], [0,1,1,1,0,1],\
#                                                  [1,0,0,1,0,1], [1,0,1,1,0,1], [1,1,0,1,0,1], [1,1,1,1,0,1]],
#                                 'outsInv_test5':[[1, 1], [0, 1]],
#                                 'outsInv_test6':[[1], [0]],
#                                 'outs_OR':      [[0], [1], [1], [1]],
#                                 'outs_AND':     [[0], [0], [0], [1]],
#                                 'outs_NOR':     [[1], [0], [0], [0]],
#                                 'outs_NAND':    [[1], [1], [1], [0]],
#                                 'outs3s_test8': [[0,0,1], [0,1,1], [1,0,1], [1,1,1]],
#                                 'outs_test9':   [[0,0,1,0,0,0], [1,0,0,0,0,1], [0,1,1,0,0,0], [1,0,1,0,0,1]],
#                                 'outs_test10':  ([0,0,0], [1,0,0], [1,0,1], [0,1,1], [1,0,1], [0,1,1], [0,1,0], [1,1,0]),
#                                 })
