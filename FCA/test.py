import context
import csv
from io.read_csv import read_csv

class C(object):
    def __init__(self):
        self.c = [0, 0]
    def get_c(self):
        return self.c[:]

if __name__ == "__main__":
    with open("some.csv", "r") as ftr:
        reader = csv.reader(ftr, delimiter=',') 
        print(next(reader))
    
    c = context.Context([[0, 0, 0, 1],
                         [1, 0, 1, 0],
                         [1, 1, 1, 0],
                         [1, 1, 1, 1]], ['ra', 'rb', 'rc', 'rd'], ['ca', 'cb', 'cc', 'cd'])
    print(c.attributes_derive(['ca', 'cb']))
    print(c.attributes_derive(['ca']))
    print(c.objects_derive(['ra']))
    print(c.objects_derive(['rd', 'rc', 'rb']))
