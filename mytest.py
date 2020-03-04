import datetime

start_time = datetime.datetime.now()

test_list = ['a', 'b', 'c', 'e', 'd']
test_list.pop(3)

for index, value in enumerate(test_list):
    print(str(index) + ') ' + value)



print(str(datetime.datetime.now() - start_time)[5:7])
print(str(datetime.datetime.now() - start_time)[2:4])