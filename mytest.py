import datetime
import kivy
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

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
for k in d1: 
    print(f'{k}: {d1[k]}')
str_d1= str(d1)
# for k in str_d1: 
#     print(f'{k}: {d1[k]}')
d2= eval(str_d1)
print(d2)