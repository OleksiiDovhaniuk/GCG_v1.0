import datetime

from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import read_configurations, read_truth_table, save_configurations, save_truth_table, autosave

def read_input_by_key(key):
    message = f'Enter value of the {key}: '
    print(message)
    value = input()
    return value

def list_2d_to_str(list_2d):
    string = ''
    for value in list_2d:
        string += '\n\t'
        string += str(value)
    return string

def time_delta_in_s(curent_time, start_time):
    time_delta = int(str(datetime.datetime.now() - start_time)[5:7])
    time_delta = time_delta + int(str(datetime.datetime.now() - start_time)[2:4])*60
    return time_delta   

configure_mode = True
while configure_mode:
    configurations = read_configurations()
    truth_table = read_truth_table()

    generations_number = configurations['iterations limit']
    generation_size = configurations['generation size']
    chromosome_size = configurations['chromosome size']
    crossover_probability = configurations['crossover probability']
    mutation_probability = configurations['mutation probability']
    memorised_number = configurations['memorised number']
    process_time = configurations['process time']
    info_delay = 1
    alpha = configurations['alpha']
    betta = configurations['betta']
    gamma = configurations['gamma']
    lamda = configurations['lamda']
    inputs = tuple(truth_table['inputs'].values())
    outputs = tuple(truth_table['outputs'].values())
    coefs = [alpha, betta, gamma, lamda]

    inputs_str = list_2d_to_str(inputs)
    outputs_str = list_2d_to_str(outputs)

    message = f'''
Truth Table:
    Inputs: {inputs_str}
    Outputs: {outputs_str}

Genetic Algorithm Configurations:
    generation size: {generation_size} (Power of the Population)
    chromosome size: {chromosome_size}
    crossover probability: {crossover_probability}
    mutation probability: {mutation_probability}
    coefs: {coefs} (Coef-s of the Fitness Function)
    memorised number: {memorised_number} (Number of Chromosomes, which will be memorised) 
    process time: {process_time} (seconds)

[Type name of the configuration to change it]...
[Type "y" to run the program]...'''

    print(message)
    input_key = input()
    if input_key in configurations:
        input_value = read_input_by_key(input_key)
        configurations[input_key] = input_value
        save_configurations(configurations)
    elif input_key in truth_table:
        input_value = read_input_by_key(input_key)
        truth_table[input_key] = input_value
        save_truth_table(configurations)
    elif input_key == 'y' or input_key == 'Y':
        configure_mode = False
start_time = datetime.datetime.now()
time_flag = datetime.datetime.now()
# genetic algorithm objects (mutable)
generation = None
ff_results = None
best_results = None
proper_results = None
time = None
results = None
# genetic algorithm objects (mutable)
generation = gntc.create_generation(generation_size, chromosome_size, len(inputs))
# ff: fitness function
ff_results = generation_result(generation, inputs, outputs, coefs)
# interation
iteration = 0
# time atributes
time = '00:00:00'
# initialise dictionary of the proper results (chromosome, FF value, search time)
proper_results = {
    'chromosome': [],
    'value': [],
    'time': []
    }
# initialise dictionary of the best results (chromosome, FF value, search time)
best_results = {
    'chromosome': [],
    'value': [],
    'time': []
    }
# add best N (N = memorised_number) chromosome to the dictionary of the best results 
for _ in range(memorised_number):
    max_ff = -1
    index_max = -1
    for index, value in enumerate(ff_results):
        if value > max_ff:
            index_max = index 
            max_ff = value
    best_results['chromosome'].append(generation[index_max])
    best_results['value'].append(max_ff)
    best_results['time'].append(time)   
    generation.pop(index_max)
    ff_results.pop(index_max)
# generate first info message of the process
max_value = -1
max_value_index = -1
for index, value in enumerate(best_results['value']):
    if value > max_value:
        max_value = value
        max_value_index = index
max_value_rounded = round(max_value, 6)
message = f'Process time {time}, current value: {max_value_rounded}'
if max_value > coefs[0]:
    message += '\n Now the best appropriate chromosome is:'
    for gene in best_results['chromosome'][max_value_index]:
        message += f'\n{gene}' 
    message += f'The search time is: {best_results["time"][max_value_index  ]}'
print(message, end='\r')
previous_massage = message
""" Make a genetic algorithm loop not included the generation 
creation and the first genectic algorithm objects setting up.
"""
while time_delta_in_s(datetime.datetime.now(), start_time) <= process_time:
    # restore "stolen" chromosome back to generation
    ff_results.extend(best_results['value'])
    generation.extend(best_results['chromosome'])
    while len(generation) > generation_size:
        min_ff = 999
        index_min = -1
        for index, value in enumerate(ff_results):
            if value < min_ff: index_max = index 
        generation.pop(index_min)
        ff_results.pop(index_min)
    # body of genetic algorithm process
    paired_parents = gntc.roulette_selection(ff_results)
    generation = gntc.crossover(generation, paired_parents, crossover_probability)
    generation = gntc.mutation(generation, mutation_probability)
    ff_results = generation_result(generation, inputs, outputs, coefs)
    # set process_time
    time = '0' + str(datetime.datetime.now() - start_time)[:7]
    # updating dictionary of the best chromosomes
    for _ in range(memorised_number):
        index_min_best = -1
        min_best_result = 999
        for index, value in enumerate(best_results['value']):
            if value < min_best_result:
                index_min_best = index 
                min_best_result = value
        max_ff = -1
        index_max = -1
        for index, value in enumerate(ff_results):
            if value > max_ff:
                index_max = index 
                max_ff = value
        if max_ff > min_best_result:
            best_results['chromosome'].pop(index_min_best)
            best_results['value'].pop(index_min_best)
            best_results['time'].pop(index_min_best)   
            best_results['chromosome'].append(generation[index_max])
            best_results['value'].append(max_ff)
            best_results['time'].append(time)   
            generation.pop(index_max)
            ff_results.pop(index_max)
    # seek for the best current chromosome
    max_value_index = -1
    max_value = -1
    for index, value in enumerate(best_results['value']):
        if value > max_value:
            max_value_index = index
            max_value = value
    # if delay time is past - reveal current results        
    if time_delta_in_s(datetime.datetime.now(), time_flag) >= info_delay:
        max_value_rounded = round(max_value, 6)
        message = f'Process time {time}, current value: {max_value_rounded}'
        if max_value > coefs[0]:
            best_chromosome = best_results['chromosome'][max_value_index] 
            if not best_chromosome in proper_results['chromosome']:
                proper_results['chromosome'].append(best_chromosome)
                proper_results['value'].append(max_value)
                proper_results['time'].append(time)
                autosave('Process Proper', proper_results, 
                    configurations, truth_table, start_time)
            search_time = best_results['time'][max_value_index]
        time_flag = datetime.datetime.now()
    print(message, end ='\r')
# the last message of the current run of the programm
max_value_index = -1
max_value = -1
for index, value in enumerate(best_results['value']):
    if value > max_value:
        max_value_index = index
        max_value = value
max_value_rounded = round(max_value, 5)
message = f'Process time {time}, current value: {max_value_rounded}'
if max_value > coefs[0]:
    message += '\nAn appropriate chromosome:'
    for gene in best_results['chromosome'][max_value_index]:
        message += f'\n{gene}' 
    search_time = best_results['time'][max_value_index]
    message += f'\nThe search time is: {search_time}'
print(f'\r{message: <{len(previous_massage)}}')
# save results to a folder in new txt-filez
if proper_results['chromosome']:
    autosave('Complete Proper', proper_results, configurations, truth_table, start_time)
else:
    autosave('Complete Best', best_results, configurations, truth_table, start_time)