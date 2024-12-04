from runner import run_data
import csv
import os

data = []
for i in range(2001, 3000):
    data.append(run_data(i))
    if i % 100 == 0:
        print(f'on: {i}')

file_exists = os.path.exists('output.csv')

with open('output.csv', 'a', newline='') as f:
    keys = data[0].keys()
    writer = csv.DictWriter(f, keys)
    if not file_exists:
        writer.writeheader()
    
    writer.writerows(data)