""" The module is a fitness functoin calculation unit.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Update: 15.01.2021

"""

import math
from timeit import timeit
from copy import deepcopy
import numpy as np
import concurrent.futures as cf
import multiprocessing as mult


def multi_calc(generation, inputs, outputs, coefs, min_q, min_d, is_ordered=True):
    args = [[chrm, inputs, outputs, coefs, min_q, min_d, is_ordered]
            for chrm in generation]
    with cf.ProcessPoolExecutor() as ex:
        results = ex.map(calc, args)

    return results
    # processes = [mult.Process(
    #     target=ff.calc,
    #     args=[
    #         chrm,
    #         inputs,
    #         entity['outputs'],
    #             [algorithm['Genetic Algorithm']['Coefficients'][coef]
    #              for coef in algorithm['Genetic Algorithm']['Coefficients']],
    #         basis['Min Quantum Cost'],
    #         basis['Min Delay']])
    #     for chrm in ga.gen]

    # for proc in processes:
    #     proc.start()

    # for proc in processes:
    #     proc.join()
    # with cf.ProcessPoolExecutor() as ex:
    #     values = [ex.submit(
    #         ff.calc,
    #         chrm=chrm,
    #         inputs=inputs,
    #         outputs=entity['outputs'],
    #         coefs=[algorithm['Genetic Algorithm']['Coefficients'][coef]
    #                for coef in algorithm['Genetic Algorithm']['Coefficients']],
    #         min_q=basis['Min Quantum Cost'],
    #         min_d=basis['Min Delay'],
    #         is_ordered=True) for chrm in ga.gen]

    #     for f in cf.as_completed(values):
    #         f.result()


def calc(chrm, inputs, outputs, coefs, min_q, min_d, is_ordered=True):
    """ Calculates fitness function values for the inputed generation.

    :arg: chrm (nested list): Given chromosome.
    Chromosome is presented as 3-dimentional nested list.
    An allele is [class <Gate>, list_of_signals_indices].

    :arg: inputs <class 'numpy.ndarray'>:
        Two-dimentional array of the input signals from truth table.

    :arg: outputs <class 'numpy.ndarray'>:
        Two-dimentional array of the output signals from truth table.

    :arg: coefs (tuple of ints): Fitness function coeficients
        in order: α, ß, γ, δ, ε.

    :arg: min_q (int): Minimal quantum cost.

    :arg: min_d (float): Minimal delay.

    :arg: is_ordered (bool): By default is False

    :return: (float): An evaluation value of the inputed chromosome.

    """
    res = res_sgn(chrm, inputs)

    if is_ordered:
        e = err_no_ordered(res, outputs)
    else:
        e = err_no(res, outputs)

    if coefs[1] == 0:
        p = 0
    else:
        p = disparity(res, inputs)

    if coefs[2] == 0:
        q = 0
    else:
        q = qcost(chrm)

    if coefs[3] == 0:
        g = 0
    else:
        g = garbage_output(chrm, inputs, outputs)

    if coefs[4] == 0:
        d = 0
    else:
        d = delay(chrm)

    return {'Fitness function': (coefs[0] * error_coef(e) +
                                 coefs[1] * parity_coef(p) +
                                 coefs[2] * qcost_coef(q, min_q) +
                                 coefs[3] * garbage_output_coef(g) +
                                 coefs[4] * delay_coef(d, min_d)),
            'Hamming distance': e,
            'Disparity': p,
            'Gate number': gate_no(chrm),
            'Quantum cost': q,
            'Delay': d,
            'Ancillary bits': g,
            }


def error_coef(errors):
    """ The error coefficient based on number of errors in system.
    The bigger is number of errors, the smaller is the value of the coefficient.
    The coefficient values are in range (0, 1].

    :arg: errors (int): Number of errors.

    :return: 1 / (errors + 1).

    """
    return 1 / (errors + 1)


def parity_coef(disparity):
    """ The parity coeficient shows who close is the circuit to
    parity concept.

    :arg: disparity (int): Number of differences of counting ones.

    :return: 1 / (disparity + 1).

    """
    return 1 / (disparity + 1)


def qcost_coef(qcost, min_qcost):
    """ The quantum cost coefficient is based on quantum cost value of the scheme.
    The bigger is number of errors, the smaller is the value of the coefficient.
    However, if the quantum cost is equal 0, the sheme is empty;
    therefore, the function result is 0.
    The coefficient values are in range [0, 1].

    :arg: qcost (int): Quantum cost value.

    :arg: min_qcost (int):
        The smallest value of the quantum cost of the scheme.
        By default it equals FREDKIN_QCOST, which is 5.

    :return: exp(-((1 - min_qcost / quanrum_cost)^2 )).

    """
    if qcost == 0:
        return 0
    else:
        x = -((1 - (min_qcost / qcost))**2)
        return math.exp(x)


def garbage_output_coef(garbage_output):
    """ The garbage output coefficient based on number of garbage outputs.
    The bigger is number of errors, the smaller is the value of the coefficient.
    The coefficient values are in range (0, 1].

    :arg: garbage_output (int): Number of garbage outputs (auxiliary inputs).

    :return: 1 / (1 + garbage_output).

    """
    return 1 / (1 + garbage_output)


def delay_coef(delay, min_delay):
    """ The delay coefficient is based on the delay value of the scheme.
    The bigger is number of errors, the smaller is the value of the coefficient.
    However, if the delay is equal 0, the scheme is empty;
    therefore, the function result will be 0.
    The coefficient values are in range [0, 1].

    :arg: delay (int): delay of a circuit.

    :arg: min_delay (int):
        the smallest value of the delay of the circuit.
        By default it equals FREDKIN_DELAY, which is 1.

    :return: exp(-( (1 - min_delay / delay)^2 )).

    Examples of execution:
        >>> [round(i_from_s(s), 3) for s in [1, 2, 25]]
        [1.0, 0.779, 0.398]

    """
    if delay == 0:
        return 0
    else:
        x = -((1 - min_delay / delay)**2)
        return math.exp(x)


def err_no(res, outputs):
    """ The function returns number of the errors for the scheme
    (also designated as chromosome, or genotype).

    :arg: res <class 'numpy.ndarray'>: Resulting signals after applying resulting scheme
        to the input signals.

    :arg: outputs <class 'numpy.ndarray'>: Output signals from the truth table.

    :return: err_no (int): Minimal number of errors in the chromosome.

    """
    this_res = np.array(res, copy=True).T
    this_outs = np.array(outputs, copy=True).T
    height = this_res.shape[0]
    width = this_outs.shape[0]
    err_map = np.array([], dtype=int)
    err_no = 0

    for row in this_outs:
        err_map = np.append(err_map, np.sum(this_res != row, 1)).copy()
    err_map = np.reshape(err_map, (width, height))

    while (err_map.shape[0] > 1):
        ind_y = np.argmax(err_map) // height
        row = err_map[ind_y]
        err_no += np.min(row)
        mins = np.min(err_map, 0)
        min_inds = np.where(row == np.min(row))
        ind_x = min_inds[0][0]
        for ind in min_inds[0][1:]:
            if mins[ind] > mins[ind_x]:
                ind_x = ind
        err_map = np.delete(err_map, ind_y, 0)
        err_map = np.delete(err_map, ind_x, 1)

    return err_no + np.min(err_map)


def err_no_ordered(res, outputs):
    """ The function returns number of the errors for the scheme
    (also designated as chromosome, or genotype).

    :arg: res <class 'numpy.ndarray'>: Resulting signals after applying resulting scheme
        to the input signals.

    :arg: outputs <class 'numpy.ndarray'>: Output signals from the truth table.

    :return: err_no (int): Number of errors in the chromosome.

    """
    this_outs = np.array(outputs, copy=True).T
    this_res = np.resize(np.array(res, copy=True).T, this_outs.shape)

    return np.sum(this_res != this_outs)


def disparity(res, inputs):
    """ The function returns numeric evaluation of the scheme disparity.

    :arg: res <class 'numpy.ndarray'>: An individual from the generation.

    :arg: inputs <class 'numpy.ndarray'>: Input signals from the truth table.

    :return: disparity (int).

    """
    return np.sum(np.sort(res) != np.sort(inputs))


def qcost(chrm):
    """ The function returns total quantum cost for the scheme.

    :arg: chrm (nested list): Given chromosome.
    Chromosome is presented as 3-dimentional nested list.
    An allele is [class <Gate>, list_of_signals_indices].

    :return: qcost (int).

    """
    qcost = 0
    for allele in chrm:
        qcost += allele[0].qcost

    return qcost


def garbage_output(chrm, inputs, outputs):
    """ The function returns number of garbage outputs/ auxillary inputs.

    :arg: chrm (nested list): Given chromosome.
    Chromosome is presented as 3-dimentional nested list.
    An allele is [class <Gate>, list_of_signals_indices].

    :arg: inputs <class 'numpy.ndarray'>: Input signals from the truth table.

    :arg: outputs <class 'numpy.ndarray'>: Output signals from the truth table.

    :return: garbage outputs number (int).

    """
    max_lines = inputs.shape[1]
    lines = np.arange(max_lines)
    garbage_no = max_lines - outputs.shape[1]
    auxillar_no = 0

    for line in inputs:
        auxillar_no += np.all(line == line[0])

    for allele in chrm:
        for ind in allele[1]:
            lines = np.delete(lines, np.where(lines == ind))

    return max(garbage_no, auxillar_no) - np.sum(lines != -1)


def delay(chrm):
    """ The function returns total delay of the scheme.

    :arg: chrm (nested list): Given chromosome.
    Chromosome is presented as 3-dimentional nested list.
    An allele is [class <Gate>, list_of_signals_indices].

    :return: delay (float).

    """
    delay = 0
    weight_list = []
    circuit_map = []

    for allele in chrm:
        if allele[0].tag != 'None':
            calc_int = np.array(allele[1])
            calc_int = 2 ** (calc_int)
            circuit_map.append(sum(calc_int))
            weight_list.append(allele[0].delay)

    max_weight = max(weight_list)
    while max_weight > 0:
        max_weight_ind = weight_list.index(max_weight)
        weights_around = []
        ind_around = []
        for ind in reversed(range(max_weight_ind)):
            if not (circuit_map[max_weight_ind] & circuit_map[ind]):
                weights_around.append(weight_list[ind])
                ind_around.append(ind)
            else:
                break
        for ind in range(max_weight_ind, len(weight_list)):
            if max_weight_ind == ind:
                continue
            if not (circuit_map[max_weight_ind] & circuit_map[ind]):
                weights_around.append(weight_list[ind])
                ind_around.append(ind)
            else:
                break

        if weights_around:
            ind_max_around = ind_around[weights_around.index(
                max(weights_around))]
            circuit_map[ind_max_around] |= circuit_map[max_weight_ind]
            weight_list[ind_max_around] = max_weight
            circuit_map.pop(max_weight_ind)
            weight_list.pop(max_weight_ind)
        else:
            delay += max_weight
            weight_list[max_weight_ind] = -1
        max_weight = max(weight_list)

    return delay


def res_sgn(chrm, inputs):
    """ The function returns result signals after completing their way through
    the circuit (chromosome).

    :arg: chrm (nested list): Given chromosome.
    Chromosome is presented as 3-dimentional nested list.
    An allele is [class <Gate>, list_of_signals_indices].

    :arg: inputs <class 'numpy.ndarray'>:
        Two-dimentional array of the input signals from truth table.

    :return: <class 'numpy.ndarray'>.

    """
    ins = np.array(inputs, copy=True)
    res = np.array([], dtype=int)
    for sset in ins:
        for allele in chrm:
            if allele[0].tag != 'None':
                to_change = sset[np.array(allele[1])]
                index = 0
                for ind, value in enumerate(to_change):
                    index += value * (2 ** ind)
                changed = allele[0].mapping[index]
                for ind, index in enumerate(allele[1]):
                    sset[index] = changed[ind]
        res = np.hstack((res, sset))

    return np.reshape(res, inputs.shape)


def gate_no(chrm):
    return len([allele for allele in chrm if allele[0].tag != 'None'])
