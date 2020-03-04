import os

relative_path_configurations = "Saves/configurations.txt"
relative_path_truth_table = "Saves/truth_table.txt"

def default_configurations():
    configurations = {
        'generation size':  400,
        'chromosome size':  7,
        'crossover chance': .2,
        'mutation chance':  .02,
        'memorised number': 5,
        'iterations limit': 1000,
        'process time':  600,
        'info delay': 20
    }
    return configurations

def default_truth_table():
    truth_table = {
        'inputs':{
            'X':    (0, 0, 0, 0, 1, 1, 1, 1),
            'Y':    (0, 0, 1, 1, 0, 0, 1, 1),
            'Ci_1': (0, 1, 0, 1, 0, 1, 0, 1),
            'A1':   (1, 1, 1, 1, 1, 1, 1, 1),
            'A2':   (0, 0, 0, 0, 0, 0, 0, 0),
            'A3':   (1, 1, 1, 1, 1, 1, 1, 1)
            },
        'outputs':{
            'S':    (0, 1, 1, 0, 1, 0, 0, 1),
            'Ci':   (0, 0, 0, 1, 0, 1, 1, 1),
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
        configurations_str += "\n{}: {}".format(key, configurations[key])
    f.write(configurations_str[1:])
    f.close

def save_truth_table(truth_table):
    f = open(relative_path_truth_table, 'w')
    truth_table_str = 'inputs:'
    for key in truth_table['inputs']:
        row = ''
        for value in truth_table['inputs'][key]:
            row += ' {}'.fornat(value)
        truth_table_str += "\n{}:{}".format(key, row)
    truth_table_str = '\noutputs:'
    for key in truth_table['outputs']:
        row = ''
        for value in truth_table['outputs'][key]:
            if value == None:
                row += ' X'
            else:
                row += ' {}'.format(value)
        truth_table_str += "\n{}:{}".format(key, row)

    f.write(truth_table_str[1:])
    f.close


def read_configurations():
    try:
        f = open (relative_path_configurations, 'r')
        if f.mode == 'r':
            configurations_str = f.read()
        configurations_str = configurations_str.split('\n')  
        if len(configurations_str) != len(default_configurations()):
            print('An error occured trying to create dictionary from the file (configurations.txt).\n{}').format(configurations_str)
            return default_configurations()
        else:
            configurations = {}
            for index, row in enumerate(configurations_str):
                row = row.split(':')
                if index == 2 or index == 3:
                    configurations[row[0]] = float(row[1].strip())
                else:
                    configurations[row[0]] = int(row[1].strip())
            return configurations
    except IOError:
        print('An error occured trying to read the file (configurations.txt).')
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
        return default_configurations()