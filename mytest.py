import datetime
import kivy
import numpy as np

start_time = datetime.datetime.now()

test_list = ['a', 'b', 'c', 'e', 'd']
test_list.pop(3)

# for index, value in enumerate(test_list):
#     print(str(index) + ') ' + value)

# print(str(datetime.datetime.now())[:19])
# print(str(datetime.datetime.now() - start_time)[2:4])

# print(kivy.__version__)

print(np.str.isdecimal('a'))
print(np.str.isdecimal('1'))
print(np.str.isdecimal('.3'))
print(np.str.isdecimal('0.3'))
print()
print(str.isnumeric('a'))
print(str.isnumeric('661'))
print(str.isnumeric('.3'))
print(np.str.isnumeric('0.3'))