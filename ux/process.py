""" It is module responsible for synthesing a scheme.

:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      23.03.2021

"""
from datetime import datetime as dt
import numpy as np
import concurrent.futures as cf
import multiprocessing as mult

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


from ux.popup import ProgressPopup
from algorithm.genetic_algorithm import GeneticAlgorithm, migration
from calc.fitness_function import calc
from component.gate import Gate
from component.node import Node
# from ux.scheme import Scheme


_collect_views = []
_report_view = None
_results = {'Device': 'Default device',
            'Genotype': (),
            'Scheme': (),
            'Fitness function': 0.0000,
            'Hamming distance': 0,
            'Disparity': 0,
            'Gate number': 0,
            'Quantum cost': 0,
            'Delay': 0,
            'Ancillary bits': 0,
            'Process flow': (),
            'Number of stagnations': 0,
            'Total process time': 0,
            'Synthesis time': 0,
            'Optimization time': 0,
            'Pause time': 0,
            'Date/time start': '',
            'Date/time end': '',
            }
_data_values = {
    'Fitness function': [[] for _ in range(3)],
    'Hamming distance': [],
    'Disparity': [],
    'Gate number': [],
    'Quantum cost': [],
    'Delay': [],
    'Ancillary bits': []}
_popup = ProgressPopup(values={key: _results[key] for key in _data_values})

FG = Gate(
    tag='FG',
    qcost=5,
    delay=5,
    nodes={
        'Control': Node('__circle_black'),
        'Target1': Node('__cross'),
        'Target2': Node('__cross')},
    mapping=[
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 1]])
NONEG = Gate(
    tag='None',
    qcost=0,
    delay=0,
    nodes={'None': Node('__dot_white_triangle_down')},
    mapping=[[0], [1]])
OPTIMASING_SCHEME = [
    [FG, [0, 4, 3]],
    [NONEG, [1]],
    [NONEG, [1]],
    [NONEG, [1]],
    [FG, [1, 0, 2]],
    [NONEG, [1]],
    [NONEG, [1]],
    [NONEG, [1]],
    [FG, [0, 3, 2]],
    [NONEG, [1]],
    [NONEG, [1]],
    [NONEG, [1]],
    [FG, [3, 0, 1]],
    [NONEG, [1]],
    [NONEG, [1]],
    [NONEG, [1]],
    [FG, [2, 0, 3]],
    [NONEG, [1]],
    [NONEG, [1]],
    [NONEG, [1]],
]
# OPTIMASING_SCHEME = [[
#     [FG, [1, 4, 3]],
#     [NONEG, [0]],
#     [NONEG, [0]],
#     [NONEG, [1]],
#     [FG, [2, 0, 1]],
#     [NONEG, [2]],
#     [NONEG, [3]],
#     [NONEG, [4]],
#     [FG, [4, 0, 1]],
#     [FG, [1, 0, 3]],
#     [NONEG, [5]],
#     [FG, [2, 0, 3]],
#     [NONEG, [0]],
#     [NONEG, [1]],
#     [NONEG, [2]],
#     [NONEG, [3]],
#     [NONEG, [4]],
#     [NONEG, [5]],
#     [NONEG, [0]],
#     [NONEG, [1]],
# ]]
# OPTIMASING_SCHEME = [
#     [NONEG, [1]],
#     [FG, [2, 6, 1]],
#     [NONEG, [1]],
#     [FG, [2, 6, 3]],
#     [FG, [7, 13, 1]],
#     [NONEG, [1]],
#     [NONEG, [1]],
#     [FG, [7, 13, 2]],
#     [NONEG, [1]],
#     [FG, [7, 13, 3]],
#     [NONEG, [1]],
#     [NONEG, [1]],
#     [FG, [9, 1, 0]],
#     [NONEG, [1]],
#     [NONEG, [1]],
#     [FG, [9, 0, 3]],
#     [NONEG, [1]],
#     [FG, [10, 0, 4]],
#     [FG, [10, 0, 5]],
#     [FG, [1, 10, 2]],
#     [FG, [3, 10, 13]],
#     [NONEG, [1]],
#     [FG, [0, 1, 3]],
#     [NONEG, [1]],
#     [FG, [13, 12, 2]],
#     [NONEG, [1]],
#     [FG, [12, 0, 10]],
#     [NONEG, [1]],
# ],
# OPTIMASING_SCHEME = [
#     [NONEG, [1]],
#     [FG, [3, 8, 1]],
#     [NONEG, [1]],
#     [FG, [5, 6, 0]],
#     [NONEG, [1]],
#     [FG, [5, 4, 1]],
#     [NONEG, [1]],
#     [FG, [9, 3, 8]],
#     [NONEG, [1]],
#     [FG, [6, 1, 2]],
#     [NONEG, [1]],
#     [FG, [3, 8, 6]],
#     [NONEG, [1]],
#     [FG, [3, 2, 8]],
#     [NONEG, [1]],
#     [FG, [1, 4, 2]],
#     [FG, [8, 6, 2]],
#     [NONEG, [1]],
#     [FG, [3, 1, 0]],
#     [NONEG, [1]],
# ]


def run(btn):
    global _results, _popup, _data_values, OPTIMASING_SCHEME
    data_values = _data_values
    _popup.open()

    _popup.title = 'Collecting data...'
    entity, basis, algorithm = _collect_data()
    max_populations = algorithm['Genetic Algorithm']['Limits']['Number of Populations']

    theta_point = max_populations
    stags = [[], {key: [] for key in data_values}]
    stagnation_no = 0
    stagnation_count = 0
    time_start = dt.now()
    synthesis_time = dt.now()
    optimization_time = dt.now()
    pause_time = 0
    is_synthesis = True
    is_optimization = False
    is_paused = False
    threshold = (
        algorithm['Genetic Algorithm']['Coefficients']['Error Coefficient'] +
        algorithm['Genetic Algorithm']['Coefficients']['Disparity Coefficient']
    )
    al_size = algorithm['Genetic Algorithm']['Sizes']['Allele Size']
    gen_size = algorithm['Genetic Algorithm']['Sizes']['Generation Size']
    island_no = algorithm['Genetic Algorithm']['Stagnation']['Number of Islands']
    island_pops = [gen_size // island_no for _ in range(island_no-1)]
    island_pops.append(gen_size - sum(island_pops))

    _popup.title = 'Initializing allgorithm...'
    islands = []
    for ga_index in range(island_no):
        islands.append(GeneticAlgorithm(
            basis=basis['Elements'],
            al_size=al_size,
            chrm_size=algorithm['Genetic Algorithm']['Sizes']['Chromosome Size'],
            gen_size=island_pops[ga_index],
            gms=algorithm['Genetic Algorithm']['Sizes']['Generation Memory Size'],
            weights=(.2, .2, .2, .4)
        ))

        islands[ga_index].create()
        # islands[ga_index].create(OPTIMASING_SCHEME)
    # islands[-1].create([OPTIMASING_SCHEME])

    population = 0
    prev_ff_value = 0
    inputs = _prep_inputs(entity['inputs'], al_size)

    _popup.title = 'Synthesis in progress...'
    while population < max_populations:
        values = {key: [] for key in data_values}
        for ga in islands:
            island_values = {key: [] for key in data_values}
            for chrm in ga.gen:
                chrm_res = calc(
                    chrm=chrm,
                    inputs=inputs,
                    outputs=entity['outputs'],
                    coefs=[algorithm['Genetic Algorithm']['Coefficients'][coef]
                           for coef in algorithm['Genetic Algorithm']['Coefficients']],
                    min_q=basis['Min Quantum Cost'],
                    min_d=basis['Min Delay'],
                    is_ordered=True)
                for key in data_values:
                    island_values[key].append(chrm_res[key])

            ga.crossover(
                values=np.array(island_values['Fitness function']),
                p=algorithm['Genetic Algorithm']['Crossover']['Probability'],
                max_length=algorithm['Genetic Algorithm']['Crossover']['Max Length'],
            )

            ga.mutation(
                values=island_values['Fitness function'],
                p=algorithm['Genetic Algorithm']['Mutation']['Probability'],
                max_length=algorithm['Genetic Algorithm']['Mutation']['Max Length'],
            )
            for key in data_values:
                values[key].extend(island_values[key])

        cur_ff_value = max(values['Fitness function'])
        # print(f'{cur_ff_value}  |  {int(population / max_populations * 100)}%')
        for key in data_values:
            if key == 'Fitness function':
                data_values[key][0].append(cur_ff_value)
                data_values[key][1].append(sum(values[key])/gen_size)
                data_values[key][2].append(min(values[key]))
            else:
                data_values[key].append(
                    values[key][values['Fitness function'].index(cur_ff_value)])

        # Display the progress
        population += 1
        update_values = {}
        for key in data_values:
            if key == 'Fitness function':
                update_values[key] = data_values[key][0][-1]
            else:
                update_values[key] = data_values[key][-1]

        _popup.update(
            progress=population / max_populations * 100,
            values={key: update_values[key] for key in update_values})

        if cur_ff_value >= threshold and is_synthesis:
            is_synthesis = False
            is_optimization = True
            synthesis_time = dt.now() - synthesis_time
            optimization_time = dt.now()
            theta_point = population
            _popup.title = 'Optimisation in progress...'

        if prev_ff_value == cur_ff_value:
            if stagnation_count >= algorithm['Genetic Algorithm']['Stagnation']['Coefficient']:
                islands = migration(
                    islands=islands,
                    values=np.array(values['Fitness function']),
                    p=algorithm['Genetic Algorithm']['Crossover']['Probability'],
                    max_length=algorithm['Genetic Algorithm']['Crossover']['Max Length'])
                stagnation_count = 0
                stagnation_no += 1
                stags[0].append(population-1)
                for key in data_values:
                    if key == 'Fitness function':
                        stags[1][key].append(data_values[key][0][-1])
                    else:
                        stags[1][key].append(data_values[key][-1])
            else:
                stagnation_count += 1
        else:
            stagnation_count = 0

        prev_ff_value = cur_ff_value

    _results['Device'] = entity['device']
    _results['Fitness function'] = round(cur_ff_value, 5)
    str_genotype = ''
    for allele in ga.gen[0]:
        str_gates = ''
        for gate in allele[1]:
            str_gates += f'{str(gate)} ,'
        str_genotype += f'[{str_gates}] '
    _results['Genotype'] = ga.gen[0]

    for key in data_values:
        if key == 'Fitness function':
            _results[key] = data_values[key][0][-1]
        else:
            _results[key] = data_values[key][-1]

    _results['Process flow'] = (
        data_values,
        stags,
        theta_point)
    _results['Number of stagnations'] = stagnation_no
    if is_synthesis:
        _results['Synthesis time'] = dt.now() - synthesis_time
        _results['Optimization time'] = dt.now() - dt.now()
    else:
        _results['Synthesis time'] = synthesis_time
        _results['Optimization time'] = dt.now() - optimization_time

    time_end = dt.now()
    _results['Total process time'] = time_end - time_start

    _results['Date/time start'] = time_start.strftime("%d-%m-%Y %H:%M:%S")
    _results['Date/time end'] = time_end.strftime("%d-%m-%Y %H:%M:%S")

    for allele in ga.gen[0]:
        print(allele[0], allele[1])

    _popup.title = 'Raising results...'
    _report_view.raise_results(_results)

    _popup.dismiss()


def set_views(views):
    """ Sets screen views for processing.

    :arg: `views`(list of View objects)

    """
    global _report_view, _collect_views
    _report_view = views[0]
    _collect_views = views[2:]


def _collect_data():
    """ Collects the inputed data.

    :return: tuple (configs, basis, entity)

    """
    global _collect_views
    return (view.get_data() for view in _collect_views)


def _prep_inputs(inputs, al_size):
    """ Adds auxiliary inputs according to allele size of the GA.

    :arg: `inputs` <numpy.ndarray>.

    :arg: `al_size` (int): Allele size (al_size >= truth table input signals).

    :return: class <numpy.ndarray>.

    """
    auxiliaries = [
        [i % 2 for i in range(len(inputs[0]), al_size)]
        for _ in inputs
    ]
    new_array = np.append(inputs, auxiliaries, axis=1)
    return np.append(inputs, auxiliaries, axis=1)
