import os, os.path
import datetime

relative_path_configurations = "saves/configurations.txt"
relative_path_truth_table = "saves/truth_table.txt"
relative_path_autosaves = "saves/autosaves/"
relative_path_messages = "res/messages/"

def default_configurations():
    configurations = {
        'generation size':  400,
        'chromosome size':  7,
        'crossover probability': .2,
        'mutation probability':  .02,
        'memorised number': 5,
        'iterations limit': 1000,
        'alpha': .91,
        'betta': .03,
        'gamma': .03,
        'lamda': .03,
        'process time':  600,
    }
    return configurations

def default_truth_table():
    truth_table = {
        'inputs':{
            'X':    (0, 0, 0, 0, 1, 1, 1, 1),
            'Y':    (0, 0, 1, 1, 0, 0, 1, 1),
            'C1':   (0, 1, 0, 1, 0, 1, 0, 1),
            'A1':   (1, 1, 1, 1, 1, 1, 1, 1),
            'A2':   (0, 0, 0, 0, 0, 0, 0, 0),
            'A3':   (1, 1, 1, 1, 1, 1, 1, 1)
            },
        'outputs':{
            'S':    (0, 1, 1, 0, 1, 0, 0, 1),
            'C2':   (0, 0, 0, 1, 0, 1, 1, 1),
            'G1':   (None, None, None, None, None, None, None, None),
            'G2':   (None, None, None, None, None, None, None, None),
            'G3':   (None, None, None, None, None, None, None, None),
            'G4':   (None, None, None, None, None, None, None, None)
            }
    }   
    return truth_table

def save_configurations(configurations):
    f = open(relative_path_configurations, 'w')
    configurations_str = ''
    for key in configurations:
        configurations_str += f'\n{key}: {configurations[key]}'
    f.write(configurations_str[1:])
    f.close

def save_truth_table(truth_table):
    f = open(relative_path_truth_table, 'w')
    truth_table_str = 'inputs:'
    for key in truth_table['inputs']:
        row = ''
        for value in truth_table['inputs'][key]:
            row += f' {value}'
        truth_table_str += f'\n{key}:{row}'
    truth_table_str = '\noutputs:'
    for key in truth_table['outputs']:
        row = ''
        for value in truth_table['outputs'][key]:
            if value == None:
                row += ' X'
            else:
                row += f' {value}'
        truth_table_str += f"\n{key}:{row}"

    f.write(truth_table_str[1:])
    f.close

def read_configurations():
    try:
        f = open (relative_path_configurations, 'r')
        if f.mode == 'r':
            configurations_str = f.read()
        configurations_str = configurations_str.split('\n')  
        if len(configurations_str) != len(default_configurations()):
            print(f'An error occured trying to create dictionary from the file configurations.txt.')
            return default_configurations()
        else:
            configurations = {}
            for index, row in enumerate(configurations_str):
                row = row.split(':')
                if (index == 2 or index == 3 or index == 6
                    or index == 7 or index == 8 or index == 9):
                    configurations[row[0]] = float(row[1].strip())
                else:
                    configurations[row[0]] = int(row[1].strip())
            return configurations
    except IOError:
        print('An error occured trying to read the file configurations.txt.')
        return default_configurations()

def read_truth_table():
    try:
        f = open (relative_path_truth_table, 'r')
        if f.mode == 'r':
            truth_table_str = f.read()
        truth_table_str = truth_table_str.split('\n')  
        truth_table = {'inputs': {}, 'outputs': {}}
        half_len = len(truth_table_str) // 2
        for row in truth_table_str[1:half_len]:
            row = row.split(':')
            values = []
            values_str = row[1].strip()
            values_str = values_str.split(' ')
            for value_str in values_str:
                values.append(int(value_str))
            truth_table['inputs'][row[0].strip()] = values
        for row in truth_table_str[half_len+1:]:
            row = row.split(':')
            values = []
            values_str = row[1].strip()
            values_str = values_str.split(' ')
            for value_str in values_str:
                if value_str == 'X':
                    values.append(None)
                else:
                    values.append(int(value_str))
            truth_table['outputs'][row[0].strip()] = values
        return truth_table
    except IOError:
        print('An error occured trying to read the file (configurations.txt).')
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
        print (f'The autosave {file_name} is removed{spaces}')
        files.pop(0)
        files_number = len(files)
    print(f'Number of autosaves - {files_number}')

def autosave(type, results, configurations, truth_table, time):
    save_datetime_str = str(time)[:19]
    save_datetime_str = save_datetime_str.replace(' ', '_')
    save_datetime_str = save_datetime_str.replace('-', '')
    save_datetime_str = save_datetime_str.replace(':', '')
    file_name = f'{save_datetime_str}.txt'

    truth_table_str = str(truth_table).replace('}', '')
    truth_table_str = truth_table_str.replace('{', '')
    truth_table_str = truth_table_str.replace("'", '')
    truth_table_str = truth_table_str.replace('], ', ']\n\t')
    truth_table_str = truth_table_str.replace('puts: ', 'puts:\n\t')
    truth_table_str = truth_table_str.replace(': [', ':\t[')

    configurations_str = str(configurations).replace('}', '')
    configurations_str = configurations_str.replace('{', '')
    configurations_str = configurations_str.replace("'", '')
    configurations_str = configurations_str.replace(', ', '\n\t')

    results_str = str(results).replace('}', '')
    results_str = results_str.replace('{', '')
    results_str = results_str.replace("'", '')
    results_str = results_str.replace(']]],', ']]]\n\n')
    results_str = results_str.replace(']],', ']]\n')
    results_str = results_str.replace(', time', '\n\ttime')
    results_str = results_str.replace('value', '\tvalue')
    results_str = results_str.replace('[[[[', '\n[[[[')

    path = f'{relative_path_autosaves}{file_name}'
    spaces = '            '
    if os.path.isfile(os.path.join(path)):
        message = f'An autosave {file_name} is rewritten{spaces}'
    else:
        message = f'An autosave {file_name} is created{spaces}'

    f = open(path, 'w+')
    results_str = f'''The {type} Results are saved in {file_name} 

Inputed Truth Table:
    {truth_table_str}

Configurations:
    {configurations_str}

Results:
    {results_str}
    '''
    f.write(results_str)
    f.close
    print(message)
    clear_autosaves()
        