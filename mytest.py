from pandas import DataFrame

mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},

          {'a': 100, 'b': 200, 'c': 300, 'd': 400},

          {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]

df = DataFrame(mydict)

print(f'{df}\n')

print(df.iloc[2, :2].values)