from kivy.config import Config
# deny to resize wondows
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
# save configurations
Config.write()
# import kivy lib
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder

from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import read_configurations, read_truth_table, save_configurations, save_truth_table, autosave

import datetime as dt
import numpy as np

# genetic algorithm objects (mutable)
generation = None
ff_results = None
best_results = None
proper_results = None
time = None
results = None
configure_mode = True
keys_float = ['crossover probability', 'mutation probability', 'alpha', 'betta', 'gamma', 'lambda']

class main_testApp(App):
    def build(self):
        root = GridLayout(cols=2, padding=50, spacing=50)

        return root

def read_input_by_key(key):
    message = f'Enter value of the {key}: '
    print(message)
    value = input()
    return value

def time_delta_in_s(curent_time, start_time):
    time_delta = int(str(dt.datetime.now() - start_time)[5:7])
    time_delta = time_delta + int(str(dt.datetime.now() - start_time)[2:4])*60
    return time_delta  

def is_valid_float(key, value):
    try:
        float_value = float(value)
        return key in keys_float and float_value <= 1
    except ValueError:
        return False

while configure_mode:
    configurations = read_configurations()
    truth_table = read_truth_table()

    generations_number = configurations['iterations limit']['value']
    generation_size = configurations['generation size']['value']
    chromosome_size = configurations['chromosome size']['value']
    crossover_probability = configurations['crossover probability']['value']
    mutation_probability = configurations['mutation probability']['value']
    memorised_number = configurations['memorised number']['value']
    process_time = configurations['process time']['value']
    info_delay = 1
    alpha = configurations['alpha']['value']
    betta = configurations['betta']['value']
    gamma = configurations['gamma']['value']
    lamda = configurations['lambda']['value']
    coefs = [alpha, betta, gamma, lamda]
    inputs = []
    for row in truth_table['inputs'].to_dict('split')['data']:
        inputs_value = []
        for value in row:
            if value == 'X':
                value = None
            inputs_value.append(value)
        inputs.append(inputs_value)
    inputs = np.array(inputs).T.tolist()
    outputs = []
    for row in truth_table['outputs'].to_dict('split')['data']:
        outputs_value = []
        for value in row:
            if value == 'X':
                value = None
            outputs_value.append(value)
        outputs.append(outputs_value)
    outputs = np.array(outputs).T.tolist()
    print(inputs)

    message = f'''
Truth Table:
    Inputs: 
{truth_table['inputs']}
    Outputs: 
{truth_table['outputs']}

Genetic Algorithm Configurations:
    generation size: {generation_size} (Power of the Population)
    chromosome size: {chromosome_size}
    crossover probability: {crossover_probability}
    mutation probability: {mutation_probability}
    coefs: {coefs} (Coef-s of the Fitness Function)
    [...to change coefs - tipe 'alpha', 'betta', 'gamma' or 'lamda' accordingly]
    memorised number: {memorised_number} (Number of Chromosomes, which will be memorised) 
    process time: {process_time} (seconds)

[Type name of the configuration to change it]...
[Type "y" to run the program]...'''.replace("'", '')

    print(message)
    input_str = input()
    # clean input from rubbish spaces
    input_reversed = input_str[::-1]
    while input_reversed[0] == ' ':
        input_reversed = input_reversed[1:]
    input_key = input_reversed[::-1]
    while input_key[0] == ' ':
        input_key = input_key[1:]
    # read a value accordingly to the inputed key    
    if input_key in configurations:
        input_value = read_input_by_key(input_key).replace(' ', '')
        if is_valid_float(input_key, input_value):
            configurations[input_key]['value'] = float(input_value)
            save_configurations(configurations)
        elif str.isdigit(input_value):
            configurations[input_key]['value'] = int(input_value)
            for key in configurations:
                print(f'{key}:{configurations[key]}')
            save_configurations(configurations)
        else:
            message = f'The value [{input_value}] is not appropriate'
            print(message,end='\r')
    elif input_key in truth_table:
        input_value = read_input_by_key(input_key)
        truth_table[input_key] = input_value
        save_truth_table(configurations)
    elif input_key == 'y' or input_key == 'Y':
        configure_mode = False
start_time = dt.datetime.now()
time_flag = dt.datetime.now()
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
while time_delta_in_s(dt.datetime.now(), start_time) <= process_time:
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
    time = '0' + str(dt.datetime.now() - start_time)[:7]
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
    if time_delta_in_s(dt.datetime.now(), time_flag) >= info_delay:
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
        time_flag = dt.datetime.now()
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


# if __name__ == '__main__':
    # main_testApp().run()
