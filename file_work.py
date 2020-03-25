import os, os.path
import datetime
from pandas import DataFrame
from numpy import array

relative_path_configurations = "saves/configurations.txt"
relative_path_truth_table = "saves/truth_table.txt"
relative_path_autosaves = "saves/autosaves/"
relative_path_messages = "res/messages/"

# error_type_style = '\033[1;30;43m'
error_type_style = ''

def default_configurations():
    configurations = {
        'generation size': {
            'value': 400, 'type': 'int', 'range': ('memorised number', 9999)},
        'chromosome size': {
            'value': 7, 'type': 'int', 'range': (2, 99)},
        'crossover probability': {
            'value':.2, 'type': 'float', 'range': (0, 1)},
        'mutation probability': {
            'value':.02, 'type': 'float', 'range': (0, 1)},
        'memorised number': {
            'value': 5, 'type': 'int', 'range': (0, 'generation size')},
        'alpha': {
            'value':.91, 'type': 'float', 'range': (0, 1)},
        'betta': {
            'value':.03, 'type': 'float', 'range': (0, 1)},
        'gamma': {
            'value':.03, 'type': 'float', 'range': (0, 1)},
        'lambda': {
            'value':.03, 'type': 'float', 'range': (0, 1)},
        'process time': {
            'value':.03, 'type': 'int', 'range': (1, 99999999999), 'active': True},
        'iterations limit': {
            'value': 1000, 'type': 'int', 'range': (1, 99999999999), 'active': False},
    }
    return configurations

def default_truth_table():
    X = 'X' # a symbol of the indefinit state
    inputs = DataFrame(columns=['X', 'Y', 'C1', 'A1', 'A2', 'A3'], 
        data=[[0, 0, 0, 1, 0, 1], 
        [0, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1]])
    outputs = DataFrame(columns=['S', 'C2', 'P', 'G1', 'G2', 'G3'],
        data=[[0, 0, 0, X, X, X],
        [1, 0, 0, X, X, X],
        [1, 0, 1, X, X, X],
        [0, 1, 1, X, X, X],
        [1, 0, 1, X, X, X],
        [0, 1, 1, X, X, X],
        [0, 1, 0, X, X, X],
        [1, 1, 0, X, X, X]])
    truth_table  = {'inputs': inputs, 'outputs': outputs}
    return truth_table

def save_configurations(configurations):
    f = open(relative_path_configurations, 'w')
    f.write(str(configurations))
    f.close

def save_truth_table(truth_table):
    f = open(relative_path_truth_table, 'w')
    truth_table_str = ''
    for key in truth_table['inputs']:
        truth_table_str += f'{key}: {truth_table["inputs"][key].tolist()}\n'
    truth_table_str = f'{truth_table_str[:len(truth_table_str)-2]}<<<split point>>>\n'
    for key in truth_table['outputs']:
        truth_table_str += f'{key}: {truth_table["outputs"][key].tolist()}\n'
    truth_table_str = f'{truth_table_str[:len(truth_table_str)-2]}'
    truth_table_str = truth_table_str.replace(']', '')
    truth_table_str = truth_table_str.replace('[', '')
    truth_table_str = truth_table_str.replace("'", '')
    f.write(truth_table_str)
    f.close

def read_configurations():
    try:
        f = open (relative_path_configurations, 'r')
        if f.mode == 'r':
            configurations_str = f.read()
            try:
                conf =  eval(configurations_str)
                for key in conf:
                    if conf[key]['type'] == 'int':
                        conf[key]['value'] = int(conf[key]['value'])
                    elif conf[key]['type'] == 'float':
                        conf[key]['value'] = float(conf[key]['value'])
                return conf
            except SyntaxError:
                print(f'{error_type_style}An error occured trying to transform dictionary from the file configurations.txt.')
                return default_configurations()
    except IOError:
        print(f'{error_type_style}An error occured trying to open the file configurations.txt.')
        return default_configurations()

def list_strs_to_df(list_strs):
    keys = []
    for rows_str in list_strs:
        keys.append(rows_str.split(': ')[0])
    values_list = []
    for rows_str in list_strs:
        values = []
        for value_str in rows_str.split(': ')[1].split(', '):
            if value_str == '0' or value_str == '1':
                values.append(int(value_str))
            else: 
                values.append(None)
        values_list.append(values)
    values_list = array(values_list).T.tolist()
    df = DataFrame(data=values_list, columns=keys)
    return df

def read_truth_table():
    try:
        f = open (relative_path_truth_table, 'r')
        if f.mode == 'r':
            truth_table_str = f.read()
            # split
            inputs_strs = truth_table_str.split('<<<split point>>>\n')[0].split('\n')
            outputs_strs = truth_table_str.split('<<<split point>>>\n')[1].split('\n')
            try:
                inputs = list_strs_to_df(inputs_strs)
                outputs = list_strs_to_df(outputs_strs)
                truth_table = {'inputs': inputs, 'outputs': outputs}
                return truth_table
            except SyntaxError:
                print(f'{error_type_style}An error occured trying to transform dictionary from truth_table.txt.')
                return default_truth_table()
    except IOError:
        print(f'{error_type_style}An error occured trying to read truth_table.txt.')
        return default_truth_table()

def clear_autosaves():
    capasity = 20
    path = relative_path_autosaves
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files_number = len(files)
    files.sort()
    while files_number > capasity:
        file_name = files[0]
        file_path = f'{path}{file_name}'
        os.remove(file_path)
        # print (f'The autosave {file_name} is removed')
        files.pop(0)
        files_number = len(files)
    # print(f'Number of autosaves - {files_number}')

def autosave(type, results, configurations, truth_table, time):
    save_datetime_str = str(time)[:19]
    save_datetime_str = save_datetime_str.replace(' ', '_')
    save_datetime_str = save_datetime_str.replace('-', '')
    save_datetime_str = save_datetime_str.replace(':', '')
    file_name = f'{save_datetime_str}.txt'

    truth_table_str = str(truth_table).replace("'", '')
    truth_table_str = truth_table_str.replace('{', '')
    truth_table_str = truth_table_str.replace('}', '')
    truth_table_str = truth_table_str.replace(', ', '\n\t')
    truth_table_str = truth_table_str.replace(':', '\n')

    configurations_str = ''
    for key in configurations:
        configurations_str += f'{key}: {configurations[key]["value"]}\n'

    results_str = f'{str(results)}______________________________________________________\n'
        
    path = f'{relative_path_autosaves}{file_name}'
    spaces = '            '
    if os.path.isfile(os.path.join(path)):
        message = f'An autosave {file_name} is rewritten{spaces}'
    else:
        message = f'An autosave {file_name} is created{spaces}'

    f = open(path, 'w+')
    results_str = f'''The {type} Results are saved in {file_name} 

    Inputed Truth Table:
------------------------
    {truth_table_str}

    Configurations:
-------------------
{configurations_str}
    Results:
------------
    {results_str}
    '''
    f.write(results_str)
    f.close
    # print(message)
    clear_autosaves()
        