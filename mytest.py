from pandas import DataFrame
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
# print(truth_table['inputs'])
