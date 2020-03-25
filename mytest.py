from pandas import DataFrame

columns = ['a', 'b', 'c']
data=[[1,2,3], [4,5,6],[7,8,9]]
df = DataFrame (columns=columns, data=data)

print(df['a'].tolist())

for index, value in enumerate(data):
    print(f'{index}: {value}')