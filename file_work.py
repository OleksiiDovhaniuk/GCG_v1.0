"""The module responses for saving/reading in/from files.

    Constans:
        DEFAULT_PATH (str),
        AUTOSAVE_PATH (str),
        DEFAULT_DATA (nested dictionary).
        
    Variables:
        _max_autosaves_no (int),
        _autosave_names (list of strs).

    Functions:
        save(data, path, indent),
        read(path),
        autosave(data).
"""
import json
import os
import os.path
from datetime import datetime


STORAGE_PATH = "saves/storage/"
DEFAULT_PATH = "saves/data.json"
AUTOSAVE_PATH = "saves/autosaves.json"
DEFAULT_DATA ={
    'Algorithm':{
        'name': 'Genetic',
        'configurations':{
            'generation size':{
                'value': 400,
                'type': 'int',
                'min': 'memorised number',
                'max': 99999999999,
                'is active': True,
                'group': 'root'
            },
            'chromosome size':{
                'value': 7,
                'type': 'int',
                'min': 2,
                'max': 99,
                'is active': True,
                'group': 'root'
            },
            'gene size':{
                'value': 6,
                'type': 'int',
                'min': 2,
                'max': 99,
                'is active': True,
                'group': 'root'
            },
            'memorised number':{
                'value': 5,
                'type': 'int',
                'min': 2,
                'max': 'generation size',
                'is active': True,
                'group': 'root'
            },
            'control gates':{
                'value': [1, 1],
                'type': 'list of ints',
                'min': 1,
                'max': 'gene size',
                'is active': True,
                'group': 'root'
            },
            'crossover probability':{
                'value': .2,
                'type': 'float',
                'min': 0,
                'max': 1,
                'is active': True,
                'group': 'root'
            },
            'mutation probability':{
                'value': .02,
                'type': 'float',
                'min': 0,
                'max': 1,
                'is active': True,
                'group': 'root'
            },
            'fitness function coeficients':{
                'value': [.91, .03, .03, .03],
                'type': 'list of float',
                'min': 0,
                'max': 1,
                'is active': True,
                'group': 'root'
            },
            'process time':{
                'value': 600,
                'type': 'int',
                'min': 1,
                'max': 99999999999,
                'is active': True,
                'group': 'process limits'
            },
            'iterations limit':{
                'value': 1000,
                'type': 'int',
                'min': 1,
                'max': 99999999999,
                'is active': False,
                'group': 'process limits'
            },
        },
    },
    'Truth Table':{
        'inputs': {
            'X': '00001111', 
            'Y': '00110011', 
            'C1': '01010101', 
        },
        'outputs': {
            'S': '01101001', 
            'C2': '00010111', 
            'P': '00111100',
        },
    },
    'Results':{

    },
    'Plot Configurations':{

    },
}

_max_autosaves_no = 5

def save(data, path=DEFAULT_PATH):
    """ Function saves  configurations` data from .json file.

    Args: 
        data: nested dictionary;
        path (str);

     Examples of execution:
        >>> save(DEFAULT_DATA, 'saves/test.json')
        >>> save(DEFAULT_DATA, 'D:1/2/saves/test2.json')
        [Errno 2] No such file or directory: 'D:1/2/saves/test2.json'
    """
    try:
        with open(path, 'w+') as f:
            json.dump(data, f, indent=4, sort_keys=False)

    except IOError as e:
        print(e)

def read(path=DEFAULT_PATH):
    """ Function reads the configurations` data from .json file.

    Args: path (str).

    Examples of execution:
        >>> read('saves/test.json')['Algorithm']['name']
        'Genetic'
        >>> read('D:1/2/saves/test2.json')['Truth Table']['outputs']['S']
        [Errno 2] No such file or directory: 'D:1/2/saves/test2.json'
        '01101001'

    """
    try:
        with open(path, 'r') as f:
            return json.load(f)

    except IOError as e:
        print(e)
        return DEFAULT_DATA

    except TypeError as e:
        print(e)
        return DEFAULT_DATA

    
def autosave(data):
    """ Adds data to autosaves.json file.

    Note: 
        if number of autosaves is bigger than `_max_autosaves_no`
        the function delets the oldest save.

    Args: 
        data: nested dictionary;
        path (str).

    Examples of execution:
        >>> autosave(DEFAULT_DATA)
        >>> saves = read(AUTOSAVE_PATH)
        >>> saves[[key for key in saves][0]]['Truth Table']['outputs']['P']
        '00111100'
    """
    autosaves = read(AUTOSAVE_PATH)
    autosaves[str(datetime.now())] = data
    
    while len(autosaves) > _max_autosaves_no:
        del autosaves[[key for key in autosaves][0]]
        
    save(autosaves, AUTOSAVE_PATH)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
