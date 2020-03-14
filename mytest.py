import datetime
import kivy
import numpy as np
from pandas import DataFrame
from nltk.tokenize import sent_tokenize, word_tokenize
import io

start_time = datetime.datetime.now()

test_list = ['a', 'b', 'c', 'e', 'd']
test_list.pop(3)

# for index, value in enumerate(test_list):
#     print(str(index) + ') ' + value)

# print(str(datetime.datetime.now())[:19])
# print(str(datetime.datetime.now() - start_time)[2:4])

# print(kivy.__version__)

d1 = {
    'generation size': {
        'value': 400, 'type': 'int'},
    'chromosome size': {
        'value': 7, 'type': 'int'},
    'crossover probability': {
        'value':.2, 'type': 'float', 'range': (0, 1)},
    'mutation probability': {
        'value':.02, 'type': 'float', 'range': (0, 1)},
    'memorised number': {
        'value': 5, 'type': 'int'},
    'iterations limit': {
        'value': 1000, 'type': 'int'},
    'alpha': {
        'value':.91, 'type': 'float', 'range': (0, 1)},
    'betta': {
        'value':.03, 'type': 'float', 'range': (0, 1)},
    'gamma': {
        'value':.03, 'type': 'float', 'range': (0, 1)},
    'lambda': {
        'value':.03, 'type': 'float', 'range': (0, 1)},
    'process time': {
        'value':.03, 'type': 'float', 'range': (0, 1)},
}
X = 'X' # a symbol of the indefinit state
inputs = DataFrame(columns=['X', 'Y', 'C1', 'A1', 'A2', 'A3', 'B3'], 
    data=[[0, 0, 0, 1, 0, 1, ], 
    [0, 0, 1, 1, 0, 1, ],
    [0, 1, 0, 1, 0, 1, ],
    [0, 1, 1, 1, 0, 1, ],
    [1, 0, 0, 1, 0, 1, ],
    [1, 0, 1, 1, 0, 1, ],
    [1, 1, 0, 1, 0, 1, ],
    [1, 1, 1, 1, 0, 1, ]])
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

def validate_truth_table_part(part):
    return part

inputs = validate_truth_table_part(truth_table['inputs'])
outputs = validate_truth_table_part(truth_table['outputs'])
truth_table_str = ''
for key in inputs:
    if inputs[key]:
        truth_table_str += f'{key}: {inputs[key].tolist()}\n'
truth_table_str = f'{truth_table_str[:len(truth_table_str)-2]}<<<split point>>>\n'
for key in outputs:
    truth_table_str += f'{key}: {outputs[key].tolist()}\n'
truth_table_str = f'{truth_table_str[:len(truth_table_str)-2]}'
truth_table_str = truth_table_str.replace('[', '')
truth_table_str = truth_table_str.replace(']', '')
print(truth_table_str)

inputs_strs = truth_table_str.split('<<<split point>>>\n')[0].split('\n')
outputs_strs = truth_table_str.split('<<<split point>>>\n')[1].split('\n')

def list_strs_to_df(list_strs):
    keys = []
    for rows_str in list_strs:
        keys.append(rows_str.split(': ')[0])
    values_list = []
    for rows_str in list_strs:
        values = []
        for value_str in rows_str.split(': ')[1].split(', '):
            try:
                values.append(int(value_str))
            except ValueError: 
                values.append('X')
        values_list.append(values)
    values_list = np.array(values_list).T.tolist()
    df = DataFrame(data=values_list, columns=keys)
    return df

new_inputs = list_strs_to_df(inputs_strs)
new_outputs = list_strs_to_df(outputs_strs)
new_truth_table = {'inputs': new_inputs, 'outputs': new_outputs}
# print()
# print(new_inputs)
# truth_table_str = truth_table_str.split('$$$')
# new_inputs = pd.DataFrame({})
# data1 = io.StringIO(truth_table_str[0])
# df1 = pd.read_csv(data1, sep='\n')
# outputs = eval(truth_table_str[1])
# for k in d1: 
#     print(f'{k}: {d1[k]}')
# str_d1= str(d1)
# for k in str_d1: 
#     print(f'{k}: {d1[k]}')
# d2= eval(str_d1)
# print(df1['X'])
# print(df1)
# print()
# # print(d2)
