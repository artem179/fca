import csv
from .. import Context

def read_csv(path, delimiter=','):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        attributes = next(reader)
        cross_table, objects = [], []
        for row in reader:
            objects.append(row[0])
            cross_table.append(list(map(int, row[1:])))
        return Context(cross_table, objects, attributes)
        
        
