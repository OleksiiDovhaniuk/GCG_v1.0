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
import datetime
import json
import os
import os.path


DEFAULT_PATH = "saves/data.json"
AUTOSAVE_PATH = "saves/autosaves.json"
DEFAULT_DATA ={
    'Algorithm Configurations':{
        'name': 'Genetic',
        'configurations':{
            'generation size':{
                'value': 400,
                'type': int,
                'min_value': 'memorised number',
                'max_value': 9999,
                'is active': True,
                'group': 'root'
            },
            'chromosome size':{
                'value': 7,
                'type': int,
                'min_value': 2,
                'max_value': 99,
                'is active': True,
                'group': 'root'
            },
            'gene size':{
                'value': 6,
                'type': int,
                'min_value': 2,
                'max_value': 99,
                'is active': True,
                'group': 'root'
            },
            'crossover probability':{
                'value': .2,
                'type': float,
                'min_value': 0,
                'max_value': 1,
                'is active': True,
                'group': 'root'
            },
            'mutation probability':{
                'value': .02,
                'type': float,
                'min_value': 0,
                'max_value': 1,
                'is active': True,
                'group': 'root'
            },
            'fitness function coeficients':{
                'value': [.91, .03, .03, .03],
                'type': list,
                'min_value': 0,
                'max_value': 1,
                'is active': True,
                'group': 'root'
            },
            'process time':{
                'value': 600,
                'type': int,
                'min_value': 1,
                'max_value': 99999999999,
                'is active': True,
                'group': 'process limits'
            },
            'iterations limit':{
                'value': 1000,
                'type': int,
                'min_value': 1,
                'max_value': 99999999999,
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

_max_autosaves_no = 20
_autosave_names = []

def save(data, path=DEFAULT_PATH, indent=4):
    """ Function saves  configurations` data from .json file.

    Args: 
        data: nested dictionary;
        path (str);
        indent (int).

    """
    try:
        f = open(path, 'w+')
        f.write(json.dumps(data, sort_keys=False, indent=indent))
        f.close()

    except IOError as e:
        print(e)
    
   
def read(path=DEFAULT_PATH):
    """ Function reads the configurations` data from .json file.

    Args: path (str).

    """
    try:
        f = open(path, 'r')
        if f.mode == 'r':
            return json.loads(f.read)

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

    """
    autosaves = read(AUTOSAVE_PATH)

    key = str(datetime.now())
    _autosave_names.append(key)
    autosaves[key] = data
    
    while len(autosaves > _max_autosaves_no):
        del autosaves[_autosave_names[0]]
        _autosave_names.pop(0)
        
    save(autosaves, AUTOSAVE_PATH, 5)