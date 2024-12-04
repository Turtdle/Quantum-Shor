from runner import run_data
import csv

data = []
for i in range(4,1000):
    data.append(run_data(i))
    if i%100 == 0:
        print(f'on: {i}')

with open('output.csv', 'w+') as f:
    keys = data[0].keys()
    writer =  csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(data)
    
