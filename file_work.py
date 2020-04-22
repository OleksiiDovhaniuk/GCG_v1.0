"""The module responses for saving/reading from files.

    Constans:
        CONFIG_PATH (str),
        TTBL_PATH (str),
        AUTOSAVE_PATH (str),
        MESSAGES_PATH (str),
        DEFAULT_CONFIGS: pandas` DataFrame, 
        DEFAILT_TTBL: dictionary of two pandas` DataFrames.

    Variables:
        _max_autosaves_no (int)

    Functions:
        save_configs(configs, path)
        save_ttbl(truth_table, path)
        read_configs(path)
        read_ttbl(path)
"""
import datetime
import os
import os.path

from pandas import DataFrame, read_csv


CONFIG_PATH = "saves/configurations.csv"
TTBL_PATH = "saves/"
AUTOSAVE_PATH = "saves/autosaves/"
MESSAGES_PATH = "res/messages/"

DEFAULT_CONFIGS = DataFrame( 
    columns=['value','type','range','active'],
    index=[
        'generation size', 
        'chromosome size',
        'gene size',
        'crossover probability',
        'mutation probability',
        'alpha',
        'betta',
        'gamma',
        'lambda',
        'progress time',
        'iterations limit'
        ], 
    data=[
        [400, int, ('memorised number', 9999), None],
        [7, int, (2, 99), None],
        [6, int, (2, 99), None],
        [.2, float, (0, 1), None],
        [.02, float, (0, 1), None],
        [.91, float, (0, 1), None],
        [.03, float, (0, 1), None],
        [.03, float, (0, 1), None],
        [.03, float, (0, 1), None],
        [600, int, (1, 99999999999), True],
        [1000, int, (1, 99999999999), False],
    ])

DEFAULT_TTBL = {
    'inputs': 
        DataFrame(index=['X', 'Y', 'C1'], 
            data=[[0, 0, 0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 0, 0 ,1, 1],
                  [0, 1, 0, 1, 0, 1, 0, 1]]),

    'outputs': DataFrame(index=['S', 'C2', 'P'],
            data=[[0, 1, 1, 0, 1, 0, 0, 1],
                  [0, 0, 0, 1, 0, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1, 0, 0]])
}

_max_autosaves_no = 20

def save_configs(configs, path=CONFIG_PATH):
    """Function saves configurations into CSV file.

    Args: 
        configs: pandas` DataFrame;
        path (str).

    """
    configs.to_csv(f'{path}.csv', index=False)

def save_ttbl(truth_table, path=TTBL_PATH):
    """Function saves the truth table into CSV files.

    Args:
        truth_table: dctionary of two pandas` DataFrames;
        path (str).

    """
    for key in truth_table:
        truth_table[key].to_csv(f'{path}/{key}.csv', index=False)
   
def read_configs(path=CONFIG_PATH):
    """Function reads the configurations from CSV file.

    Args: path (str).

    """
    try:
        return read_csv(path)

    except IOError as e:
        print(f'Error: pandas cannot read {path}.\n{e.strerror}')
        return DEFAULT_CONFIGS

def read_ttbl(path=TTBL_PATH):
    """Function reads the truth table the folder.
    The inputs from <CONFIG_PATH>/inputs.csv and
    the outputs from <CONFIG_PATH>/outputs.csv.

    Args: path (str).

    """
    truth_table = {}

    for key in ('inputs', 'outputs'):
        try:
            truth_table[key] = read_csv(f'{path}/{key}.csv.')

        except IOError as e:
            print(f'Error: pandas cannot read {path}/{key}.csv.\n{e.strerror}')
            return DEFAULT_TTBL
    
    return truth_table
            

# def clear_autosaves():
#     """ Function removes outdated autosaves` folders,
#     if the number of the autosaves is more then _max_autosaves_no.

#     """
#     folders_no = 0
#     for name in os.listdir(AUTOSAVE_PATH):
#         if os.path.isdir(f'{AUTOSAVE_PATH}/{name}'):
#             folders_no += 1

#     for name in os.listdir(AUTOSAVE_PATH):
#         if folders_no >= _max_autosaves_no:
#             if os.path.isdir(f'{AUTOSAVE_PATH}/{name}'):
#                 try:
#                     os.rmdir(f'{AUTOSAVE_PATH}/{name}')
#                 except OSError as e:
#                     print(f'Error: {AUTOSAVE_PATH}/{name} : {e.strerror}.')
#                 else:
#                     print (f'{name} is successfully removed.')

# def autosave(truth_table, results, configs, time, status):
#     """ Function automaticaly saves all nesesser information for
#     a user.

#     Args: 
#         truth_table: dictionary of two pandas` DataFrames
#         results: list of Results
#         configs: pandas` DataFrame 
#         time: process time
#         status: one of ['toDo', 'doing' , 'finish']
    
#     """
#     clear_autosaves()
#     save_time = str(datetime)

#     try:
#         os.mkdir(AUTOSAVE_PATH)
#     except OSError as e:
#         print (f'Eroor:{e.strerror}')
#     else:
#         print (f'{save_time}{status} successfully created.')
    

# class Configuration():
#     """A class represents configuration unit.

#     Instances:
#         title (str): name of the configuration;
#         value (any);
#         gap (list of ints/floats): for exhample [a, b] 
#             means that a <= value <= b;
#         status (bool).
    
#     """
#     def __init__(self, title, value, gap, status=True):
#         self.title = title
#         self.value = value
#         self.gap = gap
#         self.status = status

#     def _str__(self):
#         return f'{self.title}, '\
#                 + f'{value}, '\
#                 + f'{type(value)}, '\
#                 + f'{gap[0]}, '\
#                 + f'{gap[1]}, '\
#                 + f'{status}\n'

# (
#     Configuration('generation size', 400, ('memorised number', 9999)),
#     Configuration('chromosome size', 7, (2, 99)),
#     Configuration('gene size', 6, (2, 99)),
#     Configuration('crossover probability', .2, (0, 1)),
#     Configuration('mutation probability', .02, (0, 1)),
#     Configuration('alpha', .91, (0, 1)),
#     Configuration('betta', .03, (0, 1)),
#     Configuration('gamma', .03, (0, 1)),
#     Configuration('lambda', .03, (0, 1)),
#     Configuration('process time', 600, (1, 99999999999)),
#     Configuration('iterations limit', 1000, (1, 99999999999, False))
#     )
